@echo off
echo ========================================
echo    PEST DETECTION MODEL TRAINING
echo ========================================
echo.

REM Activate virtual environment
echo Activating virtual environment...
call pest_detect_env\Scripts\activate.bat

REM Check if data.yaml exists
if not exist "ai_model\data.yaml" (
    echo Error: data.yaml not found!
    echo Please create a data.yaml file first.
    echo See TRAINING_GUIDE.md for instructions.
    pause
    exit /b 1
)

REM Navigate to ai_model directory
cd ai_model

REM Show available options
echo.
echo Available training options:
echo 1. Quick training (50 epochs, small model)
echo 2. Standard training (100 epochs, medium model)
echo 3. Full training (200 epochs, large model)
echo 4. Custom training (specify parameters)
echo.

set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" (
    echo Starting quick training...
    python train.py --model yolov8n.pt --epochs 50 --batch 16 --device auto
) else if "%choice%"=="2" (
    echo Starting standard training...
    python train.py --model yolov8m.pt --epochs 100 --batch 16 --device auto
) else if "%choice%"=="3" (
    echo Starting full training...
    python train.py --model yolov8l.pt --epochs 200 --batch 8 --device auto
) else if "%choice%"=="4" (
    echo.
    echo Custom training options:
    echo --model: yolov8n.pt, yolov8s.pt, yolov8m.pt, yolov8l.pt, yolov8x.pt
    echo --epochs: Number of training epochs
    echo --batch: Batch size
    echo --device: cpu, cuda, or auto
    echo --imgsz: Image size (416, 640, 832)
    echo.
    set /p custom_args="Enter custom parameters: "
    python train.py %custom_args%
) else (
    echo Invalid choice. Exiting...
    pause
    exit /b 1
)

echo.
echo Training completed!
echo Check the runs/detect/pest_detection/ directory for results.
echo.

pause
