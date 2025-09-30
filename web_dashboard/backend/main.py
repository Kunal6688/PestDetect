"""
FastAPI Backend for Pest Detection Dashboard
Provides REST API endpoints for the farmer monitoring dashboard
"""

from iot_controller.actuator import PestManagementSystem
from ai_model.detect import PestDetector
from fastapi import FastAPI, HTTPException, UploadFile, File, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
import uvicorn
import json
import asyncio
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import os
import sys
from pathlib import Path

# Add parent directories to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))
sys.path.append(str(Path(__file__).parent.parent.parent / "ai_model"))
sys.path.append(str(Path(__file__).parent.parent.parent / "iot_controller"))


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Pest Detection API",
    description="API for pest detection and farm management system",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables
pest_detector = None
iot_system = None
connected_clients = []
detection_history = []

# Initialize components


@app.on_event("startup")
async def startup_event():
    """Initialize the pest detection system on startup"""
    global pest_detector, iot_system

    try:
        # Initialize pest detector
        pest_detector = PestDetector(model_path='ai_model/best.pt')
        pest_detector.load_model()

        # Initialize IoT system
        iot_system = PestManagementSystem()
        iot_system.start_system()

        logger.info("Pest detection system initialized successfully")

    except Exception as e:
        logger.error(f"Error initializing system: {e}")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    global iot_system

    if iot_system:
        iot_system.stop_system()
        logger.info("System shutdown completed")

# WebSocket connection manager


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except:
                # Remove disconnected clients
                self.active_connections.remove(connection)


manager = ConnectionManager()

# API Routes


@app.get("/api")
async def api_root():
    """API root endpoint"""
    return {"message": "Pest Detection API", "status": "running"}


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "components": {
            "pest_detector": pest_detector is not None,
            "iot_system": iot_system is not None
        }
    }


@app.post("/detect")
async def detect_pests(file: UploadFile = File(...)):
    """
    Detect pests in uploaded image

    Args:
        file: Image file to analyze

    Returns:
        Detection results
    """
    if not pest_detector:
        raise HTTPException(
            status_code=500, detail="Pest detector not initialized")

    try:
        # Save uploaded file temporarily
        temp_path = f"temp_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}"
        with open(temp_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)

        # Perform detection
        results = pest_detector.detect_image(temp_path, save_result=False)

        # Clean up temporary file
        os.remove(temp_path)

        # Store in history
        detection_history.append({
            "timestamp": datetime.now().isoformat(),
            "filename": file.filename,
            "results": results
        })

        # Keep only last 100 detections
        if len(detection_history) > 100:
            detection_history.pop(0)

        # Broadcast to connected clients
        await manager.broadcast(json.dumps({
            "type": "new_detection",
            "data": results
        }))

        return results

    except Exception as e:
        logger.error(f"Error in pest detection: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/detections")
async def get_detections(limit: int = 50):
    """
    Get recent detection history

    Args:
        limit: Maximum number of detections to return

    Returns:
        List of recent detections
    """
    return {
        "detections": detection_history[-limit:],
        "total": len(detection_history)
    }


@app.get("/system/status")
async def get_system_status():
    """Get current system status"""
    if not iot_system:
        raise HTTPException(
            status_code=500, detail="IoT system not initialized")

    try:
        status = iot_system.get_system_status()
        return status
    except Exception as e:
        logger.error(f"Error getting system status: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/system/action")
async def trigger_action(action: Dict):
    """
    Trigger a system action

    Args:
        action: Action configuration

    Returns:
        Action result
    """
    if not iot_system:
        raise HTTPException(
            status_code=500, detail="IoT system not initialized")

    try:
        iot_system.add_action(action)

        # Broadcast action to connected clients
        await manager.broadcast(json.dumps({
            "type": "action_triggered",
            "data": action
        }))

        return {"status": "success", "action": action}

    except Exception as e:
        logger.error(f"Error triggering action: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/system/pest-response")
async def trigger_pest_response(request: Dict):
    """
    Trigger automated pest response

    Args:
        request: Pest response request with pest_type, confidence, and location

    Returns:
        Response result
    """
    if not iot_system:
        raise HTTPException(
            status_code=500, detail="IoT system not initialized")

    try:
        pest_type = request.get("pest_type")
        confidence = request.get("confidence", 0.5)
        location = request.get("location", (0, 0))

        iot_system.trigger_pest_response(pest_type, confidence, location)

        return {
            "status": "success",
            "pest_type": pest_type,
            "confidence": confidence,
            "location": location
        }

    except Exception as e:
        logger.error(f"Error triggering pest response: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/sensors")
async def get_sensor_data():
    """Get current sensor data"""
    if not iot_system:
        raise HTTPException(
            status_code=500, detail="IoT system not initialized")

    try:
        sensor_data = iot_system.sensor_controller.get_all_sensor_data()
        return sensor_data
    except Exception as e:
        logger.error(f"Error getting sensor data: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/statistics")
async def get_statistics():
    """Get pest detection statistics"""
    try:
        if not detection_history:
            return {
                "total_detections": 0,
                "pest_types": {},
                "confidence_stats": {"avg": 0, "min": 0, "max": 0},
                "recent_activity": []
            }

        # Calculate statistics
        total_detections = len(detection_history)
        pest_types = {}
        confidences = []

        for detection in detection_history:
            results = detection.get("results", {})
            detections = results.get("detections", [])

            for det in detections:
                pest_type = det.get("class_name", "unknown")
                confidence = det.get("confidence", 0)

                pest_types[pest_type] = pest_types.get(pest_type, 0) + 1
                confidences.append(confidence)

        # Recent activity (last 24 hours)
        cutoff_time = datetime.now() - timedelta(hours=24)
        recent_activity = [
            d for d in detection_history
            if datetime.fromisoformat(d["timestamp"]) > cutoff_time
        ]

        return {
            "total_detections": total_detections,
            "pest_types": pest_types,
            "confidence_stats": {
                "avg": sum(confidences) / len(confidences) if confidences else 0,
                "min": min(confidences) if confidences else 0,
                "max": max(confidences) if confidences else 0
            },
            "recent_activity": len(recent_activity)
        }

    except Exception as e:
        logger.error(f"Error calculating statistics: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time updates"""
    await manager.connect(websocket)
    try:
        while True:
            # Keep connection alive and handle incoming messages
            data = await websocket.receive_text()
            message = json.loads(data)

            # Handle different message types
            if message.get("type") == "ping":
                await manager.send_personal_message(
                    json.dumps({"type": "pong"}), websocket
                )

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        logger.info("WebSocket client disconnected")

# Static files (for serving the React app)
app.mount("/static", StaticFiles(directory="web_dashboard/frontend/build/static"), name="static")


@app.get("/")
async def serve_root():
    """Serve the React dashboard at root"""
    dashboard_path = "web_dashboard/frontend/build/index.html"
    if os.path.exists(dashboard_path):
        return FileResponse(dashboard_path)
    else:
        return HTMLResponse("""
        <html>
            <head><title>Pest Detection Dashboard</title></head>
            <body>
                <h1>Pest Detection Dashboard</h1>
                <p>React frontend not built yet. Please run 'npm run build' in the frontend directory.</p>
                <p>API is available at <a href="/docs">/docs</a></p>
            </body>
        </html>
        """)


@app.get("/dashboard")
async def serve_dashboard():
    """Serve the React dashboard"""
    dashboard_path = "web_dashboard/frontend/build/index.html"
    if os.path.exists(dashboard_path):
        return FileResponse(dashboard_path)
    else:
        return HTMLResponse("""
        <html>
            <head><title>Pest Detection Dashboard</title></head>
            <body>
                <h1>Pest Detection Dashboard</h1>
                <p>React frontend not built yet. Please run 'npm run build' in the frontend directory.</p>
                <p>API is available at <a href="/docs">/docs</a></p>
            </body>
        </html>
        """)

# Catch-all route for React Router (must be last)


@app.get("/{full_path:path}")
async def serve_react_app(full_path: str):
    """Serve React app for all other routes (for client-side routing)"""
    dashboard_path = "web_dashboard/frontend/build/index.html"
    if os.path.exists(dashboard_path):
        return FileResponse(dashboard_path)
    else:
        return HTMLResponse("""
        <html>
            <head><title>Pest Detection Dashboard</title></head>
            <body>
                <h1>Pest Detection Dashboard</h1>
                <p>React frontend not built yet. Please run 'npm run build' in the frontend directory.</p>
                <p>API is available at <a href="/docs">/docs</a></p>
            </body>
        </html>
        """)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
