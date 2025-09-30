@echo off
echo Setting up Pest Detection System Environment...
echo.

REM Create virtual environment
echo Creating virtual environment...
python -m venv pest_detect_env

REM Activate virtual environment
echo Activating virtual environment...
call pest_detect_env\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install Python dependencies
echo Installing Python dependencies...
pip install -r requirements.txt

REM Install Node.js dependencies for frontend
echo Installing Node.js dependencies...
cd web_dashboard\frontend
npm install
cd ..\..

REM Build React frontend
echo Building React frontend...
cd web_dashboard\frontend
npm run build
cd ..\..

echo.
echo Environment setup complete!
echo.
echo To activate the environment in the future, run:
echo pest_detect_env\Scripts\activate.bat
echo.
echo To start the system, run:
echo python main.py
echo.
pause
