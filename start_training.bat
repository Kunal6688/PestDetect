@echo off
echo ========================================
echo    PEST DETECTION TRAINING SETUP
echo ========================================
echo.

REM Activate virtual environment
echo Activating virtual environment...
call pest_detect_env\Scripts\activate.bat

echo.
echo This script will help you prepare and train your pest detection model.
echo.

REM Check if dataset exists
if not exist "datasets\pest_dataset" (
    echo No dataset found. Let's create one!
    echo.
    echo You need to:
    echo 1. Collect images of pests (1000+ per class recommended)
    echo 2. Label them using tools like LabelImg or Roboflow
    echo 3. Organize them in the correct format
    echo.
    echo For now, let's create a sample dataset structure...
    echo.
    
    REM Create sample dataset structure
    python prepare_dataset.py --source "sample_images" --output "datasets/pest_dataset" --train-ratio 0.7 --val-ratio 0.2 --test-ratio 0.1
    
    if errorlevel 1 (
        echo.
        echo Please create a 'sample_images' directory and add some pest images with labels.
        echo Then run this script again.
        pause
        exit /b 1
    )
) else (
    echo Dataset found! Validating...
    python prepare_dataset.py --validate-only --output "datasets/pest_dataset"
)

echo.
echo Dataset is ready! Starting training...
echo.

REM Start training
cd ai_model
python train.py --data data.yaml --model yolov8n.pt --epochs 50 --batch 16 --device auto

echo.
echo Training completed! Check the results in runs/detect/pest_detection/
echo.

pause
