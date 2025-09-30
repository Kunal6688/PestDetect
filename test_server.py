#!/usr/bin/env python3
"""
Simple test server to serve the React frontend
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn
import os

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="web_dashboard/frontend/build/static"), name="static")


@app.get("/")
async def serve_react_app():
    """Serve the React dashboard at root"""
    dashboard_path = "web_dashboard/frontend/build/index.html"
    if os.path.exists(dashboard_path):
        return FileResponse(dashboard_path)
    else:
        return {"error": "React build not found", "path": dashboard_path}


@app.get("/{full_path:path}")
async def serve_react_app_catch_all(full_path: str):
    """Serve React app for all other routes (for client-side routing)"""
    dashboard_path = "web_dashboard/frontend/build/index.html"
    if os.path.exists(dashboard_path):
        return FileResponse(dashboard_path)
    else:
        return {"error": "React build not found", "path": dashboard_path}

if __name__ == "__main__":
    print("Starting test server...")
    print("React build path:", "web_dashboard/frontend/build/index.html")
    print("Static files path:", "web_dashboard/frontend/build/static")
    print("Server will be available at: http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
