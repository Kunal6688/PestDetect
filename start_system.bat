@echo off
echo Starting Pest Detection System...
echo.

REM Activate virtual environment
echo Activating virtual environment...
call pest_detect_env\Scripts\activate.bat

REM Start the system
echo Starting the system...
python main.py

pause
