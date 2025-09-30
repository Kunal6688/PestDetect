#!/usr/bin/env python3
"""
Dataset Preparation Script for Pest Detection
This script helps you organize your pest images into the correct format for YOLO training.
"""

import os
import shutil
import yaml
from pathlib import Path
import argparse
import logging

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def create_dataset_structure(base_path="datasets/pest_dataset"):
    """Create the standard YOLO dataset structure"""

    # Create directories
    directories = [
        f"{base_path}/images/train",
        f"{base_path}/images/val",
        f"{base_path}/images/test",
        f"{base_path}/labels/train",
        f"{base_path}/labels/val",
        f"{base_path}/labels/test"
    ]

    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        logger.info(f"Created directory: {directory}")

    return base_path


def create_data_yaml(dataset_path, output_path="ai_model/data.yaml"):
    """Create data.yaml configuration file"""

    data_config = {
        'train': f"{dataset_path}/images/train/",
        'val': f"{dataset_path}/images/val/",
        'test': f"{dataset_path}/images/test/",
        'nc': 10,
        'names': {
            0: 'aphid',
            1: 'whitefly',
            2: 'thrips',
            3: 'mite',
            4: 'caterpillar',
            5: 'beetle',
            6: 'grasshopper',
            7: 'leafhopper',
            8: 'scale_insect',
            9: 'mealybug'
        },
        'path': dataset_path
    }

    with open(output_path, 'w') as f:
        yaml.dump(data_config, f, default_flow_style=False)

    logger.info(f"Created data.yaml at: {output_path}")
    return output_path


def split_dataset(source_dir, dataset_path, train_ratio=0.7, val_ratio=0.2, test_ratio=0.1):
    """
    Split dataset into train/val/test sets

    Args:
        source_dir: Directory containing all images
        dataset_path: Base dataset path
        train_ratio: Ratio for training set
        val_ratio: Ratio for validation set  
        test_ratio: Ratio for test set
    """

    import random
    random.seed(42)  # For reproducible splits

    # Get all image files
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff'}
    image_files = []

    for ext in image_extensions:
        image_files.extend(Path(source_dir).glob(f"**/*{ext}"))
        image_files.extend(Path(source_dir).glob(f"**/*{ext.upper()}"))

    logger.info(f"Found {len(image_files)} images")

    # Shuffle and split
    random.shuffle(image_files)

    total = len(image_files)
    train_end = int(total * train_ratio)
    val_end = train_end + int(total * val_ratio)

    train_files = image_files[:train_end]
    val_files = image_files[train_end:val_end]
    test_files = image_files[val_end:]

    logger.info(
        f"Split: {len(train_files)} train, {len(val_files)} val, {len(test_files)} test")

    # Copy files to appropriate directories
    for files, split_name in [(train_files, 'train'), (val_files, 'val'), (test_files, 'test')]:
        for img_file in files:
            # Copy image
            dest_img = Path(dataset_path) / "images" / \
                split_name / img_file.name
            shutil.copy2(img_file, dest_img)

            # Copy corresponding label file if it exists
            label_file = img_file.with_suffix('.txt')
            if label_file.exists():
                dest_label = Path(dataset_path) / "labels" / \
                    split_name / label_file.name
                shutil.copy2(label_file, dest_label)
            else:
                logger.warning(f"No label file found for {img_file.name}")

    logger.info("Dataset split completed!")


def validate_dataset(dataset_path):
    """Validate the dataset structure and files"""

    required_dirs = [
        "images/train", "images/val", "images/test",
        "labels/train", "labels/val", "labels/test"
    ]

    issues = []

    # Check directories
    for dir_name in required_dirs:
        dir_path = Path(dataset_path) / dir_name
        if not dir_path.exists():
            issues.append(f"Missing directory: {dir_name}")

    # Check for images and labels
    for split in ['train', 'val', 'test']:
        img_dir = Path(dataset_path) / "images" / split
        label_dir = Path(dataset_path) / "labels" / split

        if img_dir.exists():
            img_files = list(img_dir.glob("*"))
            label_files = list(label_dir.glob("*.txt")
                               ) if label_dir.exists() else []

            logger.info(
                f"{split}: {len(img_files)} images, {len(label_files)} labels")

            if len(img_files) == 0:
                issues.append(f"No images in {split} set")

            if len(label_files) == 0:
                issues.append(f"No labels in {split} set")

    if issues:
        logger.error("Dataset validation failed:")
        for issue in issues:
            logger.error(f"  - {issue}")
        return False
    else:
        logger.info("Dataset validation passed!")
        return True


def main():
    parser = argparse.ArgumentParser(
        description='Prepare dataset for pest detection training')

    parser.add_argument('--source', type=str, required=True,
                        help='Source directory containing all images and labels')
    parser.add_argument('--output', type=str, default='datasets/pest_dataset',
                        help='Output dataset directory')
    parser.add_argument('--train-ratio', type=float, default=0.7,
                        help='Training set ratio')
    parser.add_argument('--val-ratio', type=float, default=0.2,
                        help='Validation set ratio')
    parser.add_argument('--test-ratio', type=float, default=0.1,
                        help='Test set ratio')
    parser.add_argument('--validate-only', action='store_true',
                        help='Only validate existing dataset')

    args = parser.parse_args()

    if args.validate_only:
        if validate_dataset(args.output):
            logger.info("Dataset is ready for training!")
        else:
            logger.error("Dataset has issues that need to be fixed.")
        return

    # Create dataset structure
    logger.info("Creating dataset structure...")
    dataset_path = create_dataset_structure(args.output)

    # Split dataset
    logger.info("Splitting dataset...")
    split_dataset(args.source, dataset_path, args.train_ratio,
                  args.val_ratio, args.test_ratio)

    # Create data.yaml
    logger.info("Creating data.yaml...")
    create_data_yaml(dataset_path)

    # Validate dataset
    logger.info("Validating dataset...")
    if validate_dataset(dataset_path):
        logger.info("Dataset preparation completed successfully!")
        logger.info(f"Dataset location: {dataset_path}")
        logger.info("You can now start training with: python ai_model/train.py")
    else:
        logger.error("Dataset preparation completed with issues.")


if __name__ == "__main__":
    main()
