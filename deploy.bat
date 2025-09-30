@echo off
echo ========================================
echo    PEST DETECTION DEPLOYMENT SETUP
echo ========================================
echo.

REM Activate virtual environment
echo Activating virtual environment...
call pest_detect_env\Scripts\activate.bat

REM Install deployment requirements
echo Installing deployment requirements...
pip install -r requirements_deploy.txt

REM Run deployment setup
echo Setting up deployment...
python deploy.py

echo.
echo ========================================
echo    DEPLOYMENT READY!
echo ========================================
echo.

echo Choose your deployment method:
echo 1. Local Preview (Streamlit)
echo 2. Heroku (Free hosting)
echo 3. Railway (Free hosting)
echo 4. Docker (Local container)
echo 5. Streamlit Cloud (Free hosting)
echo.

set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" (
    echo Starting local Streamlit app...
    streamlit run app.py
) else if "%choice%"=="2" (
    echo Setting up Heroku deployment...
    echo Please install Heroku CLI and run: heroku create your-app-name
    echo Then run: git push heroku main
) else if "%choice%"=="3" (
    echo Setting up Railway deployment...
    echo Please install Railway CLI and run: railway login
    echo Then run: railway deploy
) else if "%choice%"=="4" (
    echo Starting Docker deployment...
    docker-compose up --build
) else if "%choice%"=="5" (
    echo Setting up Streamlit Cloud...
    echo 1. Push your code to GitHub
    echo 2. Go to https://share.streamlit.io
    echo 3. Connect your GitHub repo
    echo 4. Deploy!
) else (
    echo Invalid choice. Exiting...
    pause
    exit /b 1
)

pause
