#!/usr/bin/env python3
"""
Simple Dataset Organization Script
This script helps you organize your pest images into the correct YOLO format.
"""

import os
import shutil
import random
from pathlib import Path
import argparse


def organize_images(source_dir, output_dir="datasets/pest_dataset", train_ratio=0.7, val_ratio=0.2, test_ratio=0.1):
    """
    Organize images from source directory into train/val/test structure

    Args:
        source_dir: Directory containing all your pest images
        output_dir: Output directory for organized dataset
        train_ratio: Ratio for training set (default 0.7)
        val_ratio: Ratio for validation set (default 0.2)
        test_ratio: Ratio for test set (default 0.1)
    """

    # Create output directories
    for split in ['train', 'val', 'test']:
        os.makedirs(f"{output_dir}/images/{split}", exist_ok=True)
        os.makedirs(f"{output_dir}/labels/{split}", exist_ok=True)

    # Get all image files
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff'}
    image_files = []

    source_path = Path(source_dir)
    for ext in image_extensions:
        image_files.extend(source_path.glob(f"**/*{ext}"))
        image_files.extend(source_path.glob(f"**/*{ext.upper()}"))

    print(f"Found {len(image_files)} images")

    if len(image_files) == 0:
        print("No images found! Please check your source directory.")
        return

    # Shuffle and split
    random.seed(42)  # For reproducible splits
    random.shuffle(image_files)

    total = len(image_files)
    train_end = int(total * train_ratio)
    val_end = train_end + int(total * val_ratio)

    train_files = image_files[:train_end]
    val_files = image_files[train_end:val_end]
    test_files = image_files[val_end:]

    print(
        f"Split: {len(train_files)} train, {len(val_files)} val, {len(test_files)} test")

    # Copy files
    for files, split_name in [(train_files, 'train'), (val_files, 'val'), (test_files, 'test')]:
        for img_file in files:
            # Copy image
            dest_img = Path(output_dir) / "images" / split_name / img_file.name
            shutil.copy2(img_file, dest_img)

            # Copy corresponding label file if it exists
            label_file = img_file.with_suffix('.txt')
            if label_file.exists():
                dest_label = Path(output_dir) / "labels" / \
                    split_name / label_file.name
                shutil.copy2(label_file, dest_label)
                print(
                    f"Copied {img_file.name} + {label_file.name} to {split_name}")
            else:
                print(
                    f"Copied {img_file.name} to {split_name} (no label file found)")

    print(f"\nDataset organized successfully!")
    print(f"Location: {output_dir}")
    print(f"Training images: {len(train_files)}")
    print(f"Validation images: {len(val_files)}")
    print(f"Test images: {len(test_files)}")


def create_sample_labels(dataset_dir="datasets/pest_dataset"):
    """Create sample label files for demonstration"""

    # Create sample labels for demonstration
    sample_labels = {
        "sample_aphid.txt": "0 0.5 0.3 0.2 0.4\n0 0.7 0.8 0.15 0.25",
        "sample_whitefly.txt": "1 0.4 0.6 0.1 0.15\n1 0.8 0.2 0.12 0.18",
        "sample_caterpillar.txt": "4 0.3 0.5 0.3 0.2",
        "sample_beetle.txt": "5 0.6 0.4 0.25 0.3"
    }

    for split in ['train', 'val', 'test']:
        labels_dir = Path(dataset_dir) / "labels" / split
        labels_dir.mkdir(parents=True, exist_ok=True)

        for filename, content in sample_labels.items():
            label_file = labels_dir / filename
            if not label_file.exists():
                with open(label_file, 'w') as f:
                    f.write(content)
                print(f"Created sample label: {label_file}")


def main():
    parser = argparse.ArgumentParser(
        description='Organize pest images into YOLO dataset format')
    parser.add_argument('--source', type=str, required=True,
                        help='Source directory containing all your pest images')
    parser.add_argument('--output', type=str, default='datasets/pest_dataset',
                        help='Output directory for organized dataset')
    parser.add_argument('--train-ratio', type=float, default=0.7,
                        help='Training set ratio (default: 0.7)')
    parser.add_argument('--val-ratio', type=float, default=0.2,
                        help='Validation set ratio (default: 0.2)')
    parser.add_argument('--test-ratio', type=float, default=0.1,
                        help='Test set ratio (default: 0.1)')
    parser.add_argument('--create-samples', action='store_true',
                        help='Create sample label files for demonstration')

    args = parser.parse_args()

    # Validate ratios
    if abs(args.train_ratio + args.val_ratio + args.test_ratio - 1.0) > 0.01:
        print("Error: Ratios must sum to 1.0")
        return

    # Create sample labels if requested
    if args.create_samples:
        create_sample_labels(args.output)

    # Organize images
    organize_images(args.source, args.output, args.train_ratio,
                    args.val_ratio, args.test_ratio)

    print("\nNext steps:")
    print("1. Add your pest images to the appropriate directories")
    print("2. Create label files (.txt) for each image")
    print("3. Run: python ai_model/train.py")


if __name__ == "__main__":
    main()
