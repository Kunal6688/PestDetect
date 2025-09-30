"""
YOLO Detection Script for Pest Detection
This script performs real-time pest detection using a trained YOLO model.
"""

import cv2
import torch
import numpy as np
from ultralytics import YOLO
import logging
from pathlib import Path
import json
from datetime import datetime
import time

# PyTorch 2.0.1 doesn't have the weights_only security feature

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PestDetector:
    def __init__(self, model_path='best.pt', conf_threshold=0.5, iou_threshold=0.45):
        """
        Initialize the pest detector

        Args:
            model_path (str): Path to the trained YOLO model
            conf_threshold (float): Confidence threshold for detections
            iou_threshold (float): IoU threshold for NMS
        """
        self.model_path = model_path
        self.conf_threshold = conf_threshold
        self.iou_threshold = iou_threshold
        self.model = None
        self.class_names = [
            'aphid', 'whitefly', 'thrips', 'mite', 'caterpillar',
            'beetle', 'grasshopper', 'leafhopper', 'scale_insect', 'mealybug'
        ]

    def load_model(self):
        """Load the trained YOLO model"""
        try:
            if not Path(self.model_path).exists() or Path(self.model_path).stat().st_size < 1000:
                logger.warning(
                    f"Model file {self.model_path} not found or invalid. Using default YOLOv8 model.")
                self.model = YOLO('yolov8n.pt')
            else:
                try:
                    self.model = YOLO(self.model_path)
                except Exception as model_error:
                    logger.warning(
                        f"Error loading custom model: {model_error}. Using default YOLOv8 model.")
                    self.model = YOLO('yolov8n.pt')
            logger.info(f"Loaded model: {self.model_path}")
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            # Fallback to default model
            try:
                self.model = YOLO('yolov8n.pt')
                logger.info("Using fallback YOLO model")
            except Exception as fallback_error:
                logger.error(
                    f"Failed to load fallback model: {fallback_error}")
                raise

    def detect_image(self, image_path, save_result=True, output_dir='detections'):
        """
        Detect pests in a single image

        Args:
            image_path (str): Path to the input image
            save_result (bool): Whether to save the result image
            output_dir (str): Directory to save results

        Returns:
            dict: Detection results
        """
        if self.model is None:
            self.load_model()

        try:
            # Read image
            image = cv2.imread(image_path)
            if image is None:
                raise ValueError(f"Could not read image: {image_path}")

            # Perform detection
            results = self.model(
                image,
                conf=self.conf_threshold,
                iou=self.iou_threshold,
                verbose=False
            )

            # Process results
            detections = []
            annotated_image = image.copy()

            for result in results:
                boxes = result.boxes
                if boxes is not None:
                    for box in boxes:
                        # Extract box coordinates
                        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                        confidence = box.conf[0].cpu().numpy()
                        class_id = int(box.cls[0].cpu().numpy())

                        # Get class name
                        class_name = self.class_names[class_id] if class_id < len(
                            self.class_names) else f"class_{class_id}"

                        # Store detection
                        detection = {
                            'bbox': [int(x1), int(y1), int(x2), int(y2)],
                            'confidence': float(confidence),
                            'class_id': class_id,
                            'class_name': class_name
                        }
                        detections.append(detection)

                        # Draw bounding box
                        cv2.rectangle(annotated_image, (int(x1), int(
                            y1)), (int(x2), int(y2)), (0, 255, 0), 2)

                        # Draw label
                        label = f"{class_name}: {confidence:.2f}"
                        label_size = cv2.getTextSize(
                            label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)[0]
                        cv2.rectangle(annotated_image, (int(x1), int(y1) - label_size[1] - 10),
                                      (int(x1) + label_size[0], int(y1)), (0, 255, 0), -1)
                        cv2.putText(annotated_image, label, (int(x1), int(y1) - 5),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

            # Save result if requested
            if save_result:
                os.makedirs(output_dir, exist_ok=True)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_path = os.path.join(
                    output_dir, f"detection_{timestamp}.jpg")
                cv2.imwrite(output_path, annotated_image)
                logger.info(f"Detection result saved to: {output_path}")

            # Create result summary
            result_summary = {
                'image_path': image_path,
                'timestamp': datetime.now().isoformat(),
                'total_detections': len(detections),
                'detections': detections,
                'model_path': self.model_path,
                'confidence_threshold': self.conf_threshold
            }

            return result_summary

        except Exception as e:
            logger.error(f"Error during detection: {e}")
            raise

    def detect_video(self, video_path, output_path=None, show_preview=True):
        """
        Detect pests in a video file

        Args:
            video_path (str): Path to the input video
            output_path (str): Path to save the output video
            show_preview (bool): Whether to show real-time preview
        """
        if self.model is None:
            self.load_model()

        try:
            # Open video
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                raise ValueError(f"Could not open video: {video_path}")

            # Get video properties
            fps = int(cap.get(cv2.CAP_PROP_FPS))
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

            # Setup video writer if output path is provided
            writer = None
            if output_path:
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                writer = cv2.VideoWriter(
                    output_path, fourcc, fps, (width, height))

            frame_count = 0
            total_detections = 0

            logger.info(f"Processing video: {video_path}")
            logger.info(f"FPS: {fps}, Resolution: {width}x{height}")

            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                # Perform detection on frame
                results = self.model(
                    frame, conf=self.conf_threshold, iou=self.iou_threshold, verbose=False)

                # Process detections
                frame_detections = 0
                for result in results:
                    boxes = result.boxes
                    if boxes is not None:
                        for box in boxes:
                            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                            confidence = box.conf[0].cpu().numpy()
                            class_id = int(box.cls[0].cpu().numpy())

                            class_name = self.class_names[class_id] if class_id < len(
                                self.class_names) else f"class_{class_id}"

                            # Draw bounding box
                            cv2.rectangle(frame, (int(x1), int(y1)),
                                          (int(x2), int(y2)), (0, 255, 0), 2)

                            # Draw label
                            label = f"{class_name}: {confidence:.2f}"
                            cv2.putText(frame, label, (int(x1), int(y1) - 10),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                            frame_detections += 1

                total_detections += frame_detections

                # Write frame to output video
                if writer:
                    writer.write(frame)

                # Show preview
                if show_preview:
                    cv2.imshow('Pest Detection', frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break

                frame_count += 1
                if frame_count % 100 == 0:
                    logger.info(
                        f"Processed {frame_count} frames, {total_detections} total detections")

            # Cleanup
            cap.release()
            if writer:
                writer.release()
            cv2.destroyAllWindows()

            logger.info(
                f"Video processing completed. Total frames: {frame_count}, Total detections: {total_detections}")

        except Exception as e:
            logger.error(f"Error during video detection: {e}")
            raise

    def detect_camera(self, camera_id=0, show_preview=True):
        """
        Detect pests using camera feed

        Args:
            camera_id (int): Camera ID (0 for default camera)
            show_preview (bool): Whether to show real-time preview
        """
        if self.model is None:
            self.load_model()

        try:
            # Open camera
            cap = cv2.VideoCapture(camera_id)
            if not cap.isOpened():
                raise ValueError(f"Could not open camera {camera_id}")

            logger.info(f"Starting camera detection (Camera ID: {camera_id})")
            logger.info("Press 'q' to quit")

            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                # Perform detection
                results = self.model(
                    frame, conf=self.conf_threshold, iou=self.iou_threshold, verbose=False)

                # Process and draw detections
                for result in results:
                    boxes = result.boxes
                    if boxes is not None:
                        for box in boxes:
                            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                            confidence = box.conf[0].cpu().numpy()
                            class_id = int(box.cls[0].cpu().numpy())

                            class_name = self.class_names[class_id] if class_id < len(
                                self.class_names) else f"class_{class_id}"

                            # Draw bounding box
                            cv2.rectangle(frame, (int(x1), int(y1)),
                                          (int(x2), int(y2)), (0, 255, 0), 2)

                            # Draw label
                            label = f"{class_name}: {confidence:.2f}"
                            cv2.putText(frame, label, (int(x1), int(y1) - 10),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                # Show frame
                if show_preview:
                    cv2.imshow('Pest Detection - Camera', frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break

            # Cleanup
            cap.release()
            cv2.destroyAllWindows()

        except Exception as e:
            logger.error(f"Error during camera detection: {e}")
            raise


def main():
    """Main detection function"""
    # Initialize detector
    detector = PestDetector(model_path='best.pt', conf_threshold=0.5)

    # Load model
    detector.load_model()

    # Example usage
    try:
        # Detect in image
        # detector.detect_image('test_image.jpg')

        # Detect in video
        # detector.detect_video('test_video.mp4', 'output_video.mp4')

        # Detect using camera
        detector.detect_camera(camera_id=0)

    except Exception as e:
        logger.error(f"Detection failed: {e}")


if __name__ == "__main__":
    main()
