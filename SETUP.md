# Pest Detection System - Setup Guide

This guide will help you set up the Pest Detection System on your machine.

## Prerequisites

### Required Software
- **Python 3.8 or higher** - [Download Python](https://www.python.org/downloads/)
- **Node.js 16 or higher** - [Download Node.js](https://nodejs.org/)
- **Git** (optional) - [Download Git](https://git-scm.com/)

### System Requirements
- **Windows 10/11** or **macOS 10.15+** or **Linux Ubuntu 18.04+**
- **4GB RAM minimum** (8GB recommended)
- **2GB free disk space**
- **Webcam or camera** (for real-time detection)

## Quick Setup

### Windows Users

1. **Open Command Prompt as Administrator**
2. **Navigate to the project directory**
   ```cmd
   cd "C:\Users\kunal\Desktop\PEST DETECT"
   ```
3. **Run the setup script**
   ```cmd
   setup_env.bat
   ```
4. **Start the system**
   ```cmd
   start_system.bat
   ```

### macOS/Linux Users

1. **Open Terminal**
2. **Navigate to the project directory**
   ```bash
   cd /path/to/PEST\ DETECT
   ```
3. **Make scripts executable**
   ```bash
   chmod +x setup_env.sh start_system.sh
   ```
4. **Run the setup script**
   ```bash
   ./setup_env.sh
   ```
5. **Start the system**
   ```bash
   ./start_system.sh
   ```

## Manual Setup

If the automated scripts don't work, follow these manual steps:

### Step 1: Create Virtual Environment

**Windows:**
```cmd
python -m venv pest_detect_env
pest_detect_env\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv pest_detect_env
source pest_detect_env/bin/activate
```

### Step 2: Install Python Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 3: Install Node.js Dependencies

```bash
cd web_dashboard/frontend
npm install
npm run build
cd ../..
```

### Step 4: Start the System

```bash
python main.py
```

## Verification

After setup, you should be able to:

1. **Access the web dashboard** at `http://localhost:8000`
2. **View API documentation** at `http://localhost:8000/docs`
3. **Upload images** for pest detection
4. **Monitor system status** in real-time

## Troubleshooting

### Common Issues

#### 1. Python Not Found
- **Windows**: Add Python to PATH during installation
- **macOS**: Install Xcode command line tools: `xcode-select --install`
- **Linux**: Install python3: `sudo apt install python3 python3-pip`

#### 2. Node.js Not Found
- Download and install Node.js from [nodejs.org](https://nodejs.org/)
- Verify installation: `node --version` and `npm --version`

#### 3. Permission Errors (Linux/macOS)
```bash
sudo chmod +x setup_env.sh start_system.sh
```

#### 4. Port Already in Use
- Change the port in `config.json`:
  ```json
  {
    "web_dashboard": {
      "port": 8001
    }
  }
  ```

#### 5. Missing Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### GPU Support (Optional)

For better AI performance with NVIDIA GPUs:

1. **Install CUDA toolkit** from [NVIDIA](https://developer.nvidia.com/cuda-downloads)
2. **Install PyTorch with CUDA support**:
   ```bash
   pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
   ```

### Raspberry Pi Setup

For IoT features on Raspberry Pi:

1. **Install GPIO libraries**:
   ```bash
   pip install RPi.GPIO gpiozero
   ```
2. **Enable GPIO** in Raspberry Pi configuration
3. **Update config.json** with correct GPIO pins

## Configuration

Edit `config.json` to customize:

- **AI Model**: Confidence thresholds, model path
- **IoT System**: GPIO pins, sensor settings
- **Web Dashboard**: Host, port, CORS settings
- **Detection**: Auto-detection intervals, camera settings

## Development Mode

For development with auto-reload:

```bash
# Backend with auto-reload
cd web_dashboard/backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Frontend with auto-reload (in another terminal)
cd web_dashboard/frontend
npm start
```

## Production Deployment

For production deployment:

1. **Build the frontend**:
   ```bash
   cd web_dashboard/frontend
   npm run build
   ```

2. **Use production server**:
   ```bash
   gunicorn web_dashboard.backend.main:app -w 4 -k uvicorn.workers.UvicornWorker
   ```

## Support

If you encounter issues:

1. **Check the logs** in `pest_detection.log`
2. **Verify all dependencies** are installed correctly
3. **Check system requirements** are met
4. **Review the configuration** in `config.json`

## Next Steps

After successful setup:

1. **Train your own model** using `ai_model/train.py`
2. **Configure IoT devices** for your specific hardware
3. **Customize the dashboard** for your needs
4. **Set up automated monitoring** and alerts

---

**Note**: This system is designed for educational and research purposes. For production use in commercial farming, ensure proper testing and validation of pest detection accuracy.
