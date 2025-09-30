"""
IoT Controller for Pest Detection System
Controls relays, motors, and sensors for automated pest management
"""

import time
import logging
import json
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import threading
import queue

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RelayController:
    """Controls relay modules for various actuators"""

    def __init__(self, relay_pins: List[int], gpio_module=None):
        """
        Initialize relay controller

        Args:
            relay_pins (List[int]): List of GPIO pins for relays
            gpio_module: GPIO module (RPi.GPIO, gpiozero, etc.)
        """
        self.relay_pins = relay_pins
        self.gpio = gpio_module
        self.relay_states = {pin: False for pin in relay_pins}
        self.setup_gpio()

    def setup_gpio(self):
        """Setup GPIO pins for relays"""
        try:
            if self.gpio:
                self.gpio.setmode(self.gpio.BCM)
                for pin in self.relay_pins:
                    self.gpio.setup(pin, self.gpio.OUT)
                    # Relays are active LOW
                    self.gpio.output(pin, self.gpio.HIGH)
                logger.info("GPIO setup completed for relays")
        except Exception as e:
            logger.error(f"GPIO setup failed: {e}")

    def activate_relay(self, pin: int, duration: float = None):
        """
        Activate a relay

        Args:
            pin (int): GPIO pin number
            duration (float): Duration in seconds (None for continuous)
        """
        try:
            if pin not in self.relay_pins:
                raise ValueError(f"Invalid relay pin: {pin}")

            if self.gpio:
                self.gpio.output(pin, self.gpio.LOW)  # Activate relay
            self.relay_states[pin] = True
            logger.info(f"Relay {pin} activated")

            if duration:
                threading.Timer(
                    duration, lambda: self.deactivate_relay(pin)).start()

        except Exception as e:
            logger.error(f"Error activating relay {pin}: {e}")

    def deactivate_relay(self, pin: int):
        """
        Deactivate a relay

        Args:
            pin (int): GPIO pin number
        """
        try:
            if pin not in self.relay_pins:
                raise ValueError(f"Invalid relay pin: {pin}")

            if self.gpio:
                self.gpio.output(pin, self.gpio.HIGH)  # Deactivate relay
            self.relay_states[pin] = False
            logger.info(f"Relay {pin} deactivated")

        except Exception as e:
            logger.error(f"Error deactivating relay {pin}: {e}")

    def get_relay_state(self, pin: int) -> bool:
        """Get current state of a relay"""
        return self.relay_states.get(pin, False)

    def cleanup(self):
        """Cleanup GPIO resources"""
        try:
            if self.gpio:
                for pin in self.relay_pins:
                    self.gpio.output(pin, self.gpio.HIGH)
                self.gpio.cleanup()
            logger.info("GPIO cleanup completed")
        except Exception as e:
            logger.error(f"GPIO cleanup error: {e}")


class MotorController:
    """Controls stepper and servo motors"""

    def __init__(self, motor_pins: Dict[str, List[int]], motor_type: str = "stepper"):
        """
        Initialize motor controller

        Args:
            motor_pins (Dict): Motor pin configurations
            motor_type (str): Type of motor (stepper, servo)
        """
        self.motor_pins = motor_pins
        self.motor_type = motor_type
        self.current_position = 0
        self.is_moving = False

    def move_stepper(self, steps: int, direction: int = 1, speed: float = 0.01):
        """
        Move stepper motor

        Args:
            steps (int): Number of steps to move
            direction (int): Direction (1 for forward, -1 for backward)
            speed (float): Delay between steps in seconds
        """
        try:
            self.is_moving = True
            logger.info(
                f"Moving stepper motor {steps} steps in direction {direction}")

            # Simulate stepper movement
            for step in range(steps):
                # In real implementation, control GPIO pins here
                time.sleep(speed)
                self.current_position += direction

            self.is_moving = False
            logger.info(
                f"Stepper motor movement completed. New position: {self.current_position}")

        except Exception as e:
            self.is_moving = False
            logger.error(f"Error moving stepper motor: {e}")

    def move_servo(self, angle: float, servo_id: int = 0):
        """
        Move servo motor to specific angle

        Args:
            angle (float): Target angle (0-180 degrees)
            servo_id (int): Servo motor ID
        """
        try:
            if not 0 <= angle <= 180:
                raise ValueError("Angle must be between 0 and 180 degrees")

            logger.info(f"Moving servo {servo_id} to angle {angle} degrees")

            # In real implementation, control PWM for servo
            # For simulation, just update position
            self.current_position = angle
            time.sleep(0.1)  # Simulate movement time

            logger.info(f"Servo {servo_id} moved to {angle} degrees")

        except Exception as e:
            logger.error(f"Error moving servo motor: {e}")

    def get_position(self) -> float:
        """Get current motor position"""
        return self.current_position


class SensorController:
    """Controls various sensors (temperature, humidity, soil moisture, etc.)"""

    def __init__(self, sensor_configs: Dict[str, Dict]):
        """
        Initialize sensor controller

        Args:
            sensor_configs (Dict): Sensor configurations
        """
        self.sensor_configs = sensor_configs
        self.sensor_data = {}
        self.sensor_threads = {}
        self.running = False

    def start_sensor_monitoring(self):
        """Start continuous sensor monitoring"""
        self.running = True
        for sensor_name, config in self.sensor_configs.items():
            thread = threading.Thread(
                target=self._monitor_sensor,
                args=(sensor_name, config),
                daemon=True
            )
            thread.start()
            self.sensor_threads[sensor_name] = thread
            logger.info(f"Started monitoring sensor: {sensor_name}")

    def stop_sensor_monitoring(self):
        """Stop sensor monitoring"""
        self.running = False
        for thread in self.sensor_threads.values():
            thread.join(timeout=1)
        logger.info("Sensor monitoring stopped")

    def _monitor_sensor(self, sensor_name: str, config: Dict):
        """Monitor individual sensor"""
        while self.running:
            try:
                # Simulate sensor reading
                value = self._read_sensor(sensor_name, config)
                self.sensor_data[sensor_name] = {
                    'value': value,
                    'timestamp': datetime.now().isoformat(),
                    'unit': config.get('unit', ''),
                    'status': 'ok'
                }
                time.sleep(config.get('interval', 1))
            except Exception as e:
                logger.error(f"Error reading sensor {sensor_name}: {e}")
                self.sensor_data[sensor_name] = {
                    'value': None,
                    'timestamp': datetime.now().isoformat(),
                    'unit': config.get('unit', ''),
                    'status': 'error',
                    'error': str(e)
                }
                time.sleep(5)  # Wait before retry

    def _read_sensor(self, sensor_name: str, config: Dict) -> float:
        """Read sensor value (simulated)"""
        sensor_type = config.get('type', 'analog')

        if sensor_type == 'temperature':
            # Simulate temperature reading (20-30°C)
            return round(20 + (time.time() % 10), 1)
        elif sensor_type == 'humidity':
            # Simulate humidity reading (40-80%)
            return round(40 + (time.time() % 40), 1)
        elif sensor_type == 'soil_moisture':
            # Simulate soil moisture reading (0-100%)
            return round((time.time() % 100), 1)
        elif sensor_type == 'light':
            # Simulate light intensity reading (0-1000 lux)
            return round((time.time() % 1000), 1)
        else:
            # Generic analog reading (0-1023)
            return round((time.time() % 1024), 1)

    def get_sensor_data(self, sensor_name: str = None) -> Dict:
        """Get sensor data"""
        if sensor_name:
            return self.sensor_data.get(sensor_name, {})
        return self.sensor_data.copy()

    def get_all_sensor_data(self) -> Dict:
        """Get all sensor data"""
        return self.sensor_data.copy()


class PestManagementSystem:
    """Main pest management system controller"""

    def __init__(self, config_file: str = None):
        """
        Initialize pest management system

        Args:
            config_file (str): Path to configuration file
        """
        self.config = self._load_config(config_file)
        self.relay_controller = None
        self.motor_controller = None
        self.sensor_controller = None
        self.action_queue = queue.Queue()
        self.is_running = False

        self._initialize_controllers()

    def _load_config(self, config_file: str) -> Dict:
        """Load configuration from file"""
        default_config = {
            'relay_pins': [18, 19, 20, 21],
            'motor_pins': {'stepper': [14, 15, 16, 17]},
            'sensors': {
                'temperature': {'type': 'temperature', 'unit': '°C', 'interval': 5},
                'humidity': {'type': 'humidity', 'unit': '%', 'interval': 5},
                'soil_moisture': {'type': 'soil_moisture', 'unit': '%', 'interval': 10},
                'light': {'type': 'light', 'unit': 'lux', 'interval': 5}
            },
            'pest_thresholds': {
                'high_risk': 0.8,
                'medium_risk': 0.5,
                'low_risk': 0.3
            }
        }

        if config_file and os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    user_config = json.load(f)
                default_config.update(user_config)
            except Exception as e:
                logger.error(f"Error loading config file: {e}")

        return default_config

    def _initialize_controllers(self):
        """Initialize all controllers"""
        try:
            # Initialize relay controller
            self.relay_controller = RelayController(
                self.config['relay_pins']
            )

            # Initialize motor controller
            self.motor_controller = MotorController(
                self.config['motor_pins']
            )

            # Initialize sensor controller
            self.sensor_controller = SensorController(
                self.config['sensors']
            )

            logger.info("All controllers initialized successfully")

        except Exception as e:
            logger.error(f"Error initializing controllers: {e}")
            raise

    def start_system(self):
        """Start the pest management system"""
        try:
            self.is_running = True

            # Start sensor monitoring
            self.sensor_controller.start_sensor_monitoring()

            # Start action processing thread
            action_thread = threading.Thread(
                target=self._process_actions, daemon=True)
            action_thread.start()

            logger.info("Pest management system started")

        except Exception as e:
            logger.error(f"Error starting system: {e}")
            raise

    def stop_system(self):
        """Stop the pest management system"""
        try:
            self.is_running = False

            # Stop sensor monitoring
            self.sensor_controller.stop_sensor_monitoring()

            # Cleanup GPIO
            if self.relay_controller:
                self.relay_controller.cleanup()

            logger.info("Pest management system stopped")

        except Exception as e:
            logger.error(f"Error stopping system: {e}")

    def _process_actions(self):
        """Process actions from the queue"""
        while self.is_running:
            try:
                action = self.action_queue.get(timeout=1)
                self._execute_action(action)
            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"Error processing action: {e}")

    def _execute_action(self, action: Dict):
        """Execute a specific action"""
        action_type = action.get('type')

        try:
            if action_type == 'spray_pesticide':
                self._spray_pesticide(action.get('duration', 5))
            elif action_type == 'activate_trap':
                self._activate_trap(action.get('duration', 30))
            elif action_type == 'adjust_camera':
                self._adjust_camera(action.get('angle', 90))
            elif action_type == 'emergency_shutdown':
                self._emergency_shutdown()
            else:
                logger.warning(f"Unknown action type: {action_type}")

        except Exception as e:
            logger.error(f"Error executing action {action_type}: {e}")

    def _spray_pesticide(self, duration: float):
        """Spray pesticide using relay-controlled pump"""
        logger.info(f"Spraying pesticide for {duration} seconds")
        self.relay_controller.activate_relay(
            0, duration)  # Relay 0 controls pump

    def _activate_trap(self, duration: float):
        """Activate pest trap"""
        logger.info(f"Activating pest trap for {duration} seconds")
        self.relay_controller.activate_relay(
            1, duration)  # Relay 1 controls trap

    def _adjust_camera(self, angle: float):
        """Adjust camera position using servo motor"""
        logger.info(f"Adjusting camera to {angle} degrees")
        self.motor_controller.move_servo(angle)

    def _emergency_shutdown(self):
        """Emergency shutdown of all systems"""
        logger.warning("Emergency shutdown activated")
        for pin in self.config['relay_pins']:
            self.relay_controller.deactivate_relay(pin)
        self.stop_system()

    def add_action(self, action: Dict):
        """Add action to the queue"""
        self.action_queue.put(action)

    def get_system_status(self) -> Dict:
        """Get current system status"""
        return {
            'is_running': self.is_running,
            'relay_states': {pin: self.relay_controller.get_relay_state(pin)
                             for pin in self.config['relay_pins']},
            'motor_position': self.motor_controller.get_position(),
            'sensor_data': self.sensor_controller.get_all_sensor_data(),
            'timestamp': datetime.now().isoformat()
        }

    def trigger_pest_response(self, pest_type: str, confidence: float, location: Tuple[float, float]):
        """
        Trigger automated pest response

        Args:
            pest_type (str): Type of pest detected
            confidence (float): Detection confidence (0-1)
            location (Tuple): Location coordinates (x, y)
        """
        try:
            # Determine response based on pest type and confidence
            if confidence >= self.config['pest_thresholds']['high_risk']:
                # High risk - immediate response
                actions = [
                    {'type': 'spray_pesticide', 'duration': 10},
                    {'type': 'activate_trap', 'duration': 60}
                ]
            elif confidence >= self.config['pest_thresholds']['medium_risk']:
                # Medium risk - moderate response
                actions = [
                    {'type': 'spray_pesticide', 'duration': 5},
                    {'type': 'activate_trap', 'duration': 30}
                ]
            else:
                # Low risk - minimal response
                actions = [
                    {'type': 'activate_trap', 'duration': 15}
                ]

            # Add actions to queue
            for action in actions:
                self.add_action(action)

            logger.info(
                f"Triggered pest response for {pest_type} (confidence: {confidence:.2f})")

        except Exception as e:
            logger.error(f"Error triggering pest response: {e}")


def main():
    """Main function for testing the IoT controller"""
    try:
        # Initialize pest management system
        system = PestManagementSystem()

        # Start the system
        system.start_system()

        # Simulate some actions
        time.sleep(2)

        # Test sensor data
        print("Sensor Data:")
        sensor_data = system.get_system_status()['sensor_data']
        for sensor, data in sensor_data.items():
            print(f"{sensor}: {data['value']} {data['unit']}")

        # Test pest response
        system.trigger_pest_response('aphid', 0.85, (100, 200))

        # Keep running for a while
        time.sleep(10)

        # Stop the system
        system.stop_system()

    except KeyboardInterrupt:
        logger.info("System stopped by user")
    except Exception as e:
        logger.error(f"System error: {e}")


if __name__ == "__main__":
    main()
