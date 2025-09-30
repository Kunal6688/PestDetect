# AI Model Training Guide for Pest Detection

This guide will help you train a YOLO model to detect various pests in agricultural images.

## 📋 Prerequisites

1. **Dataset**: You need a labeled dataset of pest images
2. **Hardware**: GPU recommended (CUDA-compatible) for faster training
3. **Storage**: At least 10GB free space for dataset and model files

## 🗂️ Dataset Structure

Your dataset should be organized in the following structure:

```
datasets/
├── pest_dataset/
│   ├── images/
│   │   ├── train/
│   │   │   ├── image1.jpg
│   │   │   ├── image2.jpg
│   │   │   └── ...
│   │   ├── val/
│   │   │   ├── val1.jpg
│   │   │   ├── val2.jpg
│   │   │   └── ...
│   │   └── test/ (optional)
│   │       ├── test1.jpg
│   │       └── ...
│   └── labels/
│       ├── train/
│       │   ├── image1.txt
│       │   ├── image2.txt
│       │   └── ...
│       ├── val/
│       │   ├── val1.txt
│       │   ├── val2.txt
│       │   └── ...
│       └── test/ (optional)
│           ├── test1.txt
│           └── ...
```

## 🏷️ Label Format

Each label file should contain one line per object in the image:
```
class_id center_x center_y width height
```

Where:
- `class_id`: Integer (0-9 for our 10 pest classes)
- `center_x`, `center_y`: Normalized coordinates (0-1)
- `width`, `height`: Normalized dimensions (0-1)

### Pest Classes (10 classes):
0. aphid
1. whitefly
2. thrips
3. mite
4. caterpillar
5. beetle
6. grasshopper
7. leafhopper
8. scale_insect
9. mealybug

## 🚀 Training Steps

### Step 1: Prepare Your Dataset

1. **Collect Images**: Gather 1000+ images of each pest type
2. **Label Images**: Use tools like:
   - [LabelImg](https://github.com/tzutalin/labelImg)
   - [Roboflow](https://roboflow.com/)
   - [CVAT](https://github.com/opencv/cvat)
3. **Split Dataset**: 
   - 70% training
   - 20% validation
   - 10% testing (optional)

### Step 2: Configure Training

1. **Update data.yaml**: Edit the data configuration file
2. **Choose Model Size**:
   - `yolov8n.pt`: Nano (fastest, least accurate)
   - `yolov8s.pt`: Small (good balance)
   - `yolov8m.pt`: Medium (better accuracy)
   - `yolov8l.pt`: Large (high accuracy)
   - `yolov8x.pt`: Extra Large (best accuracy, slowest)

### Step 3: Start Training

```bash
# Activate virtual environment
pest_detect_env\Scripts\activate.bat

# Run training
python ai_model/train.py --data datasets/pest_dataset/data.yaml --epochs 100 --imgsz 640
```

### Step 4: Monitor Training

- Training progress will be displayed in the terminal
- Check `runs/detect/train/` for:
  - Training plots
  - Model weights (`best.pt`, `last.pt`)
  - Validation results

## 📊 Training Parameters

### Essential Parameters:
- `--epochs`: Number of training epochs (100-300)
- `--imgsz`: Image size (416, 640, 832)
- `--batch`: Batch size (8, 16, 32)
- `--lr0`: Initial learning rate (0.01)
- `--lrf`: Final learning rate factor (0.1)

### Advanced Parameters:
- `--patience`: Early stopping patience (50)
- `--save_period`: Save checkpoint every N epochs (10)
- `--cache`: Cache images for faster training (True)
- `--device`: Training device ('cpu', '0', '0,1')

## 🔧 Training Scripts

### Basic Training:
```bash
python ai_model/train.py
```

### Custom Training:
```bash
python ai_model/train.py --data datasets/pest_dataset/data.yaml --epochs 200 --imgsz 640 --batch 16 --device 0
```

### Resume Training:
```bash
python ai_model/train.py --resume runs/detect/train/weights/last.pt
```

## 📈 Training Tips

### 1. **Data Quality**
- Use high-quality, diverse images
- Ensure proper lighting and focus
- Include various angles and backgrounds
- Balance classes (similar number of images per pest type)

### 2. **Training Strategy**
- Start with a pre-trained model
- Use data augmentation
- Monitor validation loss
- Use early stopping to prevent overfitting

### 3. **Hardware Optimization**
- Use GPU for faster training
- Increase batch size if you have more GPU memory
- Use mixed precision training

### 4. **Model Selection**
- Start with YOLOv8n for quick testing
- Use YOLOv8m or YOLOv8l for production
- Consider YOLOv8x for maximum accuracy

## 🎯 Expected Results

### Good Training Indicators:
- Training loss decreases steadily
- Validation loss follows training loss
- mAP@0.5 > 0.7 (70% accuracy)
- mAP@0.5:0.95 > 0.5 (50% accuracy)

### Model Performance:
- **Fast**: YOLOv8n - 6.2ms inference time
- **Balanced**: YOLOv8m - 8.2ms inference time
- **Accurate**: YOLOv8l - 10.1ms inference time

## 🚨 Common Issues

### 1. **Out of Memory**
- Reduce batch size
- Reduce image size
- Use gradient accumulation

### 2. **Poor Accuracy**
- Increase dataset size
- Improve data quality
- Adjust learning rate
- Use data augmentation

### 3. **Overfitting**
- Use validation split
- Add regularization
- Reduce model complexity
- Use early stopping

## 📁 Output Files

After training, you'll find:
- `best.pt`: Best model weights
- `last.pt`: Last epoch weights
- `results.png`: Training plots
- `confusion_matrix.png`: Classification results
- `val_batch0_labels.jpg`: Validation examples

## 🔄 Next Steps

1. **Test Model**: Use `ai_model/detect.py` to test on new images
2. **Deploy Model**: Copy `best.pt` to `ai_model/best.pt`
3. **Update System**: Restart the pest detection system
4. **Monitor Performance**: Track detection accuracy in production

## 📚 Additional Resources

- [YOLOv8 Documentation](https://docs.ultralytics.com/)
- [YOLO Training Guide](https://docs.ultralytics.com/modes/train/)
- [Dataset Labeling Tools](https://roboflow.com/)
- [Model Evaluation Metrics](https://docs.ultralytics.com/modes/val/)

---

**Note**: Training a good model requires patience and experimentation. Start with a small dataset to test your setup, then scale up with more data and longer training times.
