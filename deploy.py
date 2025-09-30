#!/usr/bin/env python3
"""
Deployment Script for Pest Detection System
This script helps deploy the project to various cloud platforms
"""

import os
import subprocess
import sys
from pathlib import Path
import json


def check_requirements():
    """Check if required packages are installed"""
    required_packages = [
        'streamlit',
        'fastapi',
        'uvicorn',
        'torch',
        'ultralytics',
        'opencv-python',
        'numpy',
        'pandas',
        'matplotlib',
        'seaborn',
        'plotly'
    ]

    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)

    if missing_packages:
        print(f"Missing packages: {', '.join(missing_packages)}")
        print("Installing missing packages...")
        subprocess.run([sys.executable, '-m', 'pip',
                       'install'] + missing_packages)

    print("All requirements satisfied!")


def create_demo_data():
    """Create demo data for the preview"""
    print("Creating demo data...")

    # Create demo detection history
    demo_data = {
        "detection_history": [
            {
                "timestamp": "2024-09-30 10:30:00",
                "pest_type": "Aphid",
                "confidence": 0.87,
                "image_name": "demo_aphid.jpg"
            },
            {
                "timestamp": "2024-09-30 11:15:00",
                "pest_type": "Whitefly",
                "confidence": 0.73,
                "image_name": "demo_whitefly.jpg"
            },
            {
                "timestamp": "2024-09-30 12:00:00",
                "pest_type": "Caterpillar",
                "confidence": 0.91,
                "image_name": "demo_caterpillar.jpg"
            }
        ]
    }

    with open("demo_data.json", "w") as f:
        json.dump(demo_data, f, indent=2)

    print("Demo data created!")


def create_streamlit_config():
    """Create Streamlit configuration"""
    config_dir = Path.home() / ".streamlit"
    config_dir.mkdir(exist_ok=True)

    config = {
        "theme": {
            "primaryColor": "#2E8B57",
            "backgroundColor": "#FFFFFF",
            "secondaryBackgroundColor": "#F0F2F6",
            "textColor": "#262730"
        },
        "server": {
            "port": 8501,
            "headless": True
        }
    }

    with open(config_dir / "config.toml", "w") as f:
        f.write("[theme]\n")
        for key, value in config["theme"].items():
            f.write(f"{key} = \"{value}\"\n")
        f.write("\n[server]\n")
        for key, value in config["server"].items():
            f.write(f"{key} = {value}\n")

    print("Streamlit config created!")


def create_heroku_files():
    """Create files needed for Heroku deployment"""
    print("Creating Heroku deployment files...")

    # Procfile
    with open("Procfile", "w") as f:
        f.write(
            "web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0\n")

    # runtime.txt
    with open("runtime.txt", "w") as f:
        f.write("python-3.11.0\n")

    # .gitignore
    gitignore_content = """
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
env.bak/
venv.bak/

# AI Models
*.pt
*.pth
*.onnx

# Data
datasets/
*.jpg
*.jpeg
*.png
*.bmp

# Logs
*.log
logs/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Streamlit
.streamlit/
"""

    with open(".gitignore", "w") as f:
        f.write(gitignore_content)

    print("Heroku files created!")


def create_docker_files():
    """Create Docker files for containerized deployment"""
    print("Creating Docker files...")

    # Dockerfile
    dockerfile_content = """
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    libgl1-mesa-glx \\
    libglib2.0-0 \\
    libsm6 \\
    libxext6 \\
    libxrender-dev \\
    libgomp1 \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements_deploy.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements_deploy.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p datasets/pest_dataset/images/train
RUN mkdir -p datasets/pest_dataset/images/val
RUN mkdir -p datasets/pest_dataset/images/test
RUN mkdir -p datasets/pest_dataset/labels/train
RUN mkdir -p datasets/pest_dataset/labels/val
RUN mkdir -p datasets/pest_dataset/labels/test

# Expose port
EXPOSE 8501

# Run the application
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
"""

    with open("Dockerfile", "w") as f:
        f.write(dockerfile_content)

    # docker-compose.yml
    compose_content = """
version: '3.8'

services:
  pest-detection:
    build: .
    ports:
      - "8501:8501"
    environment:
      - PYTHONPATH=/app
    volumes:
      - ./datasets:/app/datasets
      - ./ai_model:/app/ai_model
    restart: unless-stopped
"""

    with open("docker-compose.yml", "w") as f:
        f.write(compose_content)

    print("Docker files created!")


def create_railway_config():
    """Create Railway deployment configuration"""
    print("Creating Railway configuration...")

    railway_config = {
        "build": {
            "builder": "NIXPACKS"
        },
        "deploy": {
            "startCommand": "streamlit run app.py --server.port=$PORT --server.address=0.0.0.0",
            "restartPolicyType": "ON_FAILURE",
            "restartPolicyMaxRetries": 10
        }
    }

    with open("railway.json", "w") as f:
        json.dump(railway_config, f, indent=2)

    print("Railway config created!")


def main():
    """Main deployment setup function"""
    print("PEST DETECTION DEPLOYMENT SETUP")
    print("=" * 50)

    # Check requirements
    check_requirements()

    # Create demo data
    create_demo_data()

    # Create Streamlit config
    create_streamlit_config()

    # Create deployment files
    create_heroku_files()
    create_docker_files()
    create_railway_config()

    print("\nDeployment setup completed!")
    print("\nAvailable deployment options:")
    print("1. Local Streamlit: streamlit run app.py")
    print("2. Heroku: git push heroku main")
    print("3. Railway: railway deploy")
    print("4. Docker: docker-compose up")
    print("5. Streamlit Cloud: Connect GitHub repo")

    print("\nQuick start:")
    print("streamlit run app.py")


if __name__ == "__main__":
    main()
