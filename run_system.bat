@echo off
echo Starting Pest Detection System...
echo.

REM Navigate to the project directory
cd /d "C:\Users\kunal\Desktop\PEST DETECT"

REM Activate virtual environment and run the system
pest_detect_env\Scripts\python.exe main.py

pause
