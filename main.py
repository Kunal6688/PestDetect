"""
Main Orchestrator for Pest Detection System
Coordinates AI model, IoT controller, and web dashboard
"""

from fastapi import FastAPI
import uvicorn
from iot_controller.actuator import PestManagementSystem
from ai_model.detect import PestDetector
import os
import sys
import time
import logging
import threading
import signal
from datetime import datetime
from pathlib import Path

# Add subdirectories to path
sys.path.append(str(Path(__file__).parent / "ai_model"))
sys.path.append(str(Path(__file__).parent / "iot_controller"))
sys.path.append(str(Path(__file__).parent / "web_dashboard" / "backend"))


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('pest_detection.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class PestDetectionOrchestrator:
    """Main orchestrator class that coordinates all system components"""

    def __init__(self, config_file=None):
        """
        Initialize the pest detection orchestrator

        Args:
            config_file (str): Path to configuration file
        """
        self.config_file = config_file
        self.ai_detector = None
        self.iot_system = None
        self.web_app = None
        self.is_running = False
        self.detection_thread = None
        self.web_thread = None

        # Load configuration
        self.config = self._load_config()

        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

    def _load_config(self):
        """Load configuration from file or use defaults"""
        default_config = {
            'ai_model': {
                'model_path': 'ai_model/best.pt',
                'confidence_threshold': 0.5,
                'iou_threshold': 0.45
            },
            'iot_system': {
                'relay_pins': [18, 19, 20, 21],
                'motor_pins': {'stepper': [14, 15, 16, 17]},
                'sensors': {
                    'temperature': {'type': 'temperature', 'unit': '°C', 'interval': 5},
                    'humidity': {'type': 'humidity', 'unit': '%', 'interval': 5},
                    'soil_moisture': {'type': 'soil_moisture', 'unit': '%', 'interval': 10},
                    'light': {'type': 'light', 'unit': 'lux', 'interval': 5}
                }
            },
            'web_dashboard': {
                'host': '0.0.0.0',
                'port': 8000,
                'reload': False
            },
            'detection': {
                'auto_detection_interval': 30,  # seconds
                'camera_id': 0,
                'enable_auto_response': True
            }
        }

        if self.config_file and os.path.exists(self.config_file):
            try:
                import json
                with open(self.config_file, 'r') as f:
                    user_config = json.load(f)
                # Merge configurations
                for key, value in user_config.items():
                    if key in default_config and isinstance(value, dict):
                        default_config[key].update(value)
                    else:
                        default_config[key] = value
                logger.info(f"Loaded configuration from {self.config_file}")
            except Exception as e:
                logger.error(f"Error loading config file: {e}")

        return default_config

    def _signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        logger.info(
            f"Received signal {signum}, initiating graceful shutdown...")
        self.stop()
        sys.exit(0)

    def initialize_components(self):
        """Initialize all system components"""
        try:
            logger.info("Initializing pest detection system components...")

            # Initialize AI detector
            logger.info("Initializing AI detector...")
            self.ai_detector = PestDetector(
                model_path=self.config['ai_model']['model_path'],
                conf_threshold=self.config['ai_model']['confidence_threshold'],
                iou_threshold=self.config['ai_model']['iou_threshold']
            )
            self.ai_detector.load_model()
            logger.info("AI detector initialized successfully")

            # Initialize IoT system
            logger.info("Initializing IoT system...")
            self.iot_system = PestManagementSystem()
            self.iot_system.start_system()
            logger.info("IoT system initialized successfully")

            # Initialize web dashboard
            logger.info("Initializing web dashboard...")
            self._initialize_web_dashboard()
            logger.info("Web dashboard initialized successfully")

            logger.info("All components initialized successfully")
            return True

        except Exception as e:
            logger.error(f"Error initializing components: {e}")
            return False

    def _initialize_web_dashboard(self):
        """Initialize the web dashboard"""
        try:
            # Import the FastAPI app
            from web_dashboard.backend.main import app

            # Store the app for later use
            self.web_app = app

            # Start web server in a separate thread
            self.web_thread = threading.Thread(
                target=self._run_web_server,
                daemon=True
            )
            self.web_thread.start()

        except Exception as e:
            logger.error(f"Error initializing web dashboard: {e}")
            raise

    def _run_web_server(self):
        """Run the web server"""
        try:
            uvicorn.run(
                self.web_app,
                host=self.config['web_dashboard']['host'],
                port=self.config['web_dashboard']['port'],
                reload=self.config['web_dashboard']['reload'],
                log_level="info"
            )
        except Exception as e:
            logger.error(f"Error running web server: {e}")

    def start_auto_detection(self):
        """Start automatic pest detection using camera"""
        if not self.config['detection']['enable_auto_response']:
            logger.info("Auto detection disabled in configuration")
            return

        def auto_detect_loop():
            logger.info("Starting automatic pest detection loop")
            while self.is_running:
                try:
                    # Perform detection using camera
                    logger.info("Performing automatic pest detection...")

                    # In a real implementation, you would capture from camera
                    # For now, we'll simulate detection
                    self._simulate_detection()

                    # Wait for next detection cycle
                    time.sleep(self.config['detection']
                               ['auto_detection_interval'])

                except Exception as e:
                    logger.error(f"Error in auto detection loop: {e}")
                    time.sleep(10)  # Wait before retrying

        self.detection_thread = threading.Thread(
            target=auto_detect_loop, daemon=True)
        self.detection_thread.start()
        logger.info("Auto detection started")

    def _simulate_detection(self):
        """Simulate pest detection for demonstration"""
        try:
            # Simulate random pest detection
            import random

            # Random chance of detecting pests
            if random.random() < 0.3:  # 30% chance
                pest_types = ['aphid', 'whitefly',
                              'thrips', 'mite', 'caterpillar']
                pest_type = random.choice(pest_types)
                confidence = random.uniform(0.6, 0.95)
                location = (random.randint(0, 640), random.randint(0, 480))

                logger.info(
                    f"Simulated detection: {pest_type} (confidence: {confidence:.2f})")

                # Trigger IoT response
                if self.iot_system:
                    self.iot_system.trigger_pest_response(
                        pest_type, confidence, location)

        except Exception as e:
            logger.error(f"Error in simulated detection: {e}")

    def detect_pests_from_image(self, image_path):
        """
        Detect pests in a specific image

        Args:
            image_path (str): Path to the image file

        Returns:
            dict: Detection results
        """
        if not self.ai_detector:
            raise RuntimeError("AI detector not initialized")

        try:
            logger.info(f"Detecting pests in image: {image_path}")
            results = self.ai_detector.detect_image(image_path)

            # Trigger IoT response if pests detected
            if results.get('total_detections', 0) > 0 and self.iot_system:
                for detection in results.get('detections', []):
                    pest_type = detection.get('class_name', 'unknown')
                    confidence = detection.get('confidence', 0)
                    bbox = detection.get('bbox', [0, 0, 0, 0])
                    location = ((bbox[0] + bbox[2]) / 2,
                                (bbox[1] + bbox[3]) / 2)

                    self.iot_system.trigger_pest_response(
                        pest_type, confidence, location)

            return results

        except Exception as e:
            logger.error(f"Error detecting pests in image: {e}")
            raise

    def get_system_status(self):
        """Get current system status"""
        status = {
            'timestamp': datetime.now().isoformat(),
            'is_running': self.is_running,
            'components': {
                'ai_detector': self.ai_detector is not None,
                'iot_system': self.iot_system is not None,
                'web_dashboard': self.web_app is not None
            }
        }

        if self.iot_system:
            status['iot_status'] = self.iot_system.get_system_status()

        return status

    def start(self):
        """Start the pest detection system"""
        try:
            logger.info("Starting Pest Detection System...")

            # Initialize all components
            if not self.initialize_components():
                logger.error("Failed to initialize components")
                return False

            # Mark as running
            self.is_running = True

            # Start auto detection if enabled
            self.start_auto_detection()

            logger.info("Pest Detection System started successfully")
            logger.info(
                f"Web dashboard available at: http://{self.config['web_dashboard']['host']}:{self.config['web_dashboard']['port']}")

            return True

        except Exception as e:
            logger.error(f"Error starting system: {e}")
            return False

    def stop(self):
        """Stop the pest detection system"""
        try:
            logger.info("Stopping Pest Detection System...")

            # Mark as not running
            self.is_running = False

            # Stop IoT system
            if self.iot_system:
                self.iot_system.stop_system()
                logger.info("IoT system stopped")

            # Wait for threads to finish
            if self.detection_thread and self.detection_thread.is_alive():
                self.detection_thread.join(timeout=5)
                logger.info("Detection thread stopped")

            logger.info("Pest Detection System stopped successfully")

        except Exception as e:
            logger.error(f"Error stopping system: {e}")

    def run_interactive_mode(self):
        """Run the system in interactive mode"""
        try:
            if not self.start():
                logger.error("Failed to start system")
                return

            logger.info("System is running. Press Ctrl+C to stop.")

            # Keep the main thread alive
            while self.is_running:
                time.sleep(1)

        except KeyboardInterrupt:
            logger.info("Received keyboard interrupt")
        finally:
            self.stop()


def main():
    """Main function"""
    import argparse

    parser = argparse.ArgumentParser(
        description='Pest Detection System Orchestrator')
    parser.add_argument('--config', '-c', help='Configuration file path')
    parser.add_argument(
        '--detect', '-d', help='Detect pests in specific image file')
    parser.add_argument('--status', '-s', action='store_true',
                        help='Show system status')

    args = parser.parse_args()

    # Create orchestrator
    orchestrator = PestDetectionOrchestrator(config_file=args.config)

    try:
        if args.detect:
            # Single image detection mode
            if not orchestrator.initialize_components():
                logger.error("Failed to initialize components")
                sys.exit(1)

            results = orchestrator.detect_pests_from_image(args.detect)
            print(f"Detection results: {results}")

        elif args.status:
            # Status check mode
            if not orchestrator.initialize_components():
                logger.error("Failed to initialize components")
                sys.exit(1)

            status = orchestrator.get_system_status()
            print(f"System status: {status}")

        else:
            # Interactive mode
            orchestrator.run_interactive_mode()

    except Exception as e:
        logger.error(f"Error in main: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
