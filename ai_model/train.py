"""
YOLO Training Script for Pest Detection
This script trains a YOLO model to detect various pests in agricultural images.

Usage:
    python train.py --data data.yaml --epochs 100 --imgsz 640
    python train.py --help  # See all options
"""

import os
import torch
import yaml
import argparse
from ultralytics import YOLO
from pathlib import Path
import logging
import shutil

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class PestDetectionTrainer:
    def __init__(self, model_size='yolov8n.pt', data_config='data.yaml'):
        """
        Initialize the pest detection trainer

        Args:
            model_size (str): YOLO model size (yolov8n.pt, yolov8s.pt, yolov8m.pt, yolov8l.pt, yolov8x.pt)
            data_config (str): Path to data configuration file
        """
        self.model_size = model_size
        self.data_config = data_config
        self.model = None

    def load_model(self):
        """Load the YOLO model"""
        try:
            self.model = YOLO(self.model_size)
            logger.info(f"Loaded YOLO model: {self.model_size}")
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            raise

    def create_data_config(self, train_path, val_path, test_path=None, num_classes=10):
        """
        Create data configuration file for YOLO training

        Args:
            train_path (str): Path to training images
            val_path (str): Path to validation images
            test_path (str): Path to test images (optional)
            num_classes (int): Number of pest classes
        """
        data_config = {
            'path': os.path.dirname(train_path),
            'train': os.path.basename(train_path),
            'val': os.path.basename(val_path),
            'nc': num_classes,
            'names': [
                'aphid', 'whitefly', 'thrips', 'mite', 'caterpillar',
                'beetle', 'grasshopper', 'leafhopper', 'scale_insect', 'mealybug'
            ]
        }

        if test_path:
            data_config['test'] = os.path.basename(test_path)

        with open(self.data_config, 'w') as f:
            yaml.dump(data_config, f, default_flow_style=False)

        logger.info(f"Created data configuration: {self.data_config}")

    def train(self, epochs=100, imgsz=640, batch=16, device='cpu', workers=8):
        """
        Train the YOLO model

        Args:
            epochs (int): Number of training epochs
            imgsz (int): Image size for training
            batch (int): Batch size
            device (str): Device to use for training ('cpu', 'cuda', or specific GPU)
            workers (int): Number of worker threads
        """
        if self.model is None:
            self.load_model()

        try:
            # Check if CUDA is available
            if device == 'cuda' and not torch.cuda.is_available():
                logger.warning("CUDA not available, falling back to CPU")
                device = 'cpu'

            logger.info(f"Starting training with {epochs} epochs...")
            logger.info(
                f"Device: {device}, Batch size: {batch}, Image size: {imgsz}")

            # Train the model
            results = self.model.train(
                data=self.data_config,
                epochs=epochs,
                imgsz=imgsz,
                batch=batch,
                device=device,
                workers=workers,
                project='runs/train',
                name='pest_detection',
                exist_ok=True,
                save=True,
                save_period=10,
                val=True,
                plots=True
            )

            logger.info("Training completed successfully!")
            logger.info(f"Best model saved to: {self.model.trainer.best}")

            return results

        except Exception as e:
            logger.error(f"Error during training: {e}")
            raise

    def validate(self, model_path=None):
        """
        Validate the trained model

        Args:
            model_path (str): Path to the trained model (if None, uses current model)
        """
        if model_path:
            model = YOLO(model_path)
        elif self.model:
            model = self.model
        else:
            raise ValueError("No model available for validation")

        try:
            logger.info("Starting validation...")
            results = model.val(data=self.data_config)
            logger.info("Validation completed!")
            return results
        except Exception as e:
            logger.error(f"Error during validation: {e}")
            raise


def main():
    """Main function with command-line interface"""
    parser = argparse.ArgumentParser(
        description='Train YOLO model for pest detection')

    # Data configuration
    parser.add_argument('--data', type=str, default='data.yaml',
                        help='Path to data configuration file')
    parser.add_argument('--model', type=str, default='yolov8n.pt',
                        choices=['yolov8n.pt', 'yolov8s.pt',
                                 'yolov8m.pt', 'yolov8l.pt', 'yolov8x.pt'],
                        help='YOLO model size')

    # Training parameters
    parser.add_argument('--epochs', type=int, default=100,
                        help='Number of training epochs')
    parser.add_argument('--imgsz', type=int, default=640,
                        help='Image size for training')
    parser.add_argument('--batch', type=int, default=16,
                        help='Batch size')
    parser.add_argument('--device', type=str, default='auto',
                        help='Device to use (cpu, cuda, or specific GPU)')
    parser.add_argument('--workers', type=int, default=8,
                        help='Number of worker threads')

    # Advanced parameters
    parser.add_argument('--patience', type=int, default=50,
                        help='Early stopping patience')
    parser.add_argument('--save-period', type=int, default=10,
                        help='Save checkpoint every N epochs')
    parser.add_argument('--cache', action='store_true', default=True,
                        help='Cache images for faster training')
    parser.add_argument('--resume', type=str, default=None,
                        help='Resume training from checkpoint')

    # Learning rate parameters
    parser.add_argument('--lr0', type=float, default=0.01,
                        help='Initial learning rate')
    parser.add_argument('--lrf', type=float, default=0.1,
                        help='Final learning rate factor')

    # Data augmentation
    parser.add_argument('--augment', action='store_true', default=True,
                        help='Enable data augmentation')
    parser.add_argument('--mixup', type=float, default=0.0,
                        help='Mixup augmentation probability')
    parser.add_argument('--copy-paste', type=float, default=0.0,
                        help='Copy-paste augmentation probability')

    args = parser.parse_args()

    # Validate data config exists
    if not os.path.exists(args.data):
        logger.error(f"Data configuration file not found: {args.data}")
        logger.info(
            "Please create a data.yaml file or specify the correct path")
        logger.info("See TRAINING_GUIDE.md for more information")
        return

    # Create trainer
    trainer = PestDetectionTrainer(
        model_size=args.model,
        data_config=args.data
    )

    # Load model
    try:
        trainer.load_model()
    except Exception as e:
        logger.error(f"Failed to load model: {e}")
        return

    # Prepare training arguments
    train_kwargs = {
        'epochs': args.epochs,
        'imgsz': args.imgsz,
        'batch': args.batch,
        'device': args.device,
        'workers': args.workers,
        'patience': args.patience,
        'save_period': args.save_period,
        'cache': args.cache,
        'lr0': args.lr0,
        'lrf': args.lrf,
        'augment': args.augment,
        'mixup': args.mixup,
        'copy_paste': args.copy_paste
    }

    # Add resume if specified
    if args.resume:
        train_kwargs['resume'] = args.resume

    # Start training
    try:
        logger.info("=" * 50)
        logger.info("PEST DETECTION MODEL TRAINING")
        logger.info("=" * 50)
        logger.info(f"Model: {args.model}")
        logger.info(f"Data: {args.data}")
        logger.info(f"Epochs: {args.epochs}")
        logger.info(f"Image size: {args.imgsz}")
        logger.info(f"Batch size: {args.batch}")
        logger.info(f"Device: {args.device}")
        logger.info("=" * 50)

        results = trainer.train(**train_kwargs)

        logger.info("=" * 50)
        logger.info("TRAINING COMPLETED SUCCESSFULLY!")
        logger.info("=" * 50)
        logger.info(f"Best model: runs/detect/pest_detection/weights/best.pt")
        logger.info(f"Last model: runs/detect/pest_detection/weights/last.pt")
        logger.info(f"Results: runs/detect/pest_detection/")
        logger.info("=" * 50)

    except Exception as e:
        logger.error(f"Training failed: {e}")
        raise


if __name__ == "__main__":
    main()
