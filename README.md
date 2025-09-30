# Pest Detection System

An intelligent pest detection system that combines AI-powered computer vision, IoT sensors, and automated response mechanisms to help farmers monitor and manage pest infestations in their crops.

## 🌟 Features

- **AI-Powered Detection**: Uses YOLO (You Only Look Once) deep learning model to detect various pest types
- **Real-time Monitoring**: Web dashboard for real-time system monitoring and control
- **IoT Integration**: Automated sensors and actuators for environmental monitoring and pest response
- **Automated Response**: Automatic triggering of pest control measures based on detection results
- **Data Analytics**: Comprehensive statistics and trend analysis
- **Multi-platform Support**: Works on Raspberry Pi, desktop, and cloud environments

## 🏗️ System Architecture

```
pest detect/
│
├── ai_model/              # AI module (YOLO training & inference)
│   ├── train.py           # Model training script
│   ├── detect.py          # Detection inference script
│   └── best.pt            # Trained model file
│
├── iot_controller/        # IoT (relay, motor, sensors)
│   └── actuator.py        # Hardware control and sensor management
│
├── web_dashboard/         # Farmer monitoring dashboard
│   ├── backend/           # FastAPI backend
│   │   └── main.py        # REST API server
│   └── frontend/          # React frontend
│       ├── src/
│       │   ├── components/
│       │   └── App.js
│       └── package.json
│
├── main.py                # Orchestrator (connects AI + IoT + Web)
├── requirements.txt       # Python dependencies
├── config.json           # System configuration
└── README.md             # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher (for React frontend)
- Camera or image input device
- Raspberry Pi (optional, for IoT features)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd pest-detect
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Node.js dependencies (for web dashboard)**
   ```bash
   cd web_dashboard/frontend
   npm install
   ```

4. **Build React frontend**
   ```bash
   npm run build
   cd ../..
   ```

5. **Configure the system**
   ```bash
   cp config.json.example config.json
   # Edit config.json with your settings
   ```

🚀 How to Run the System:
Option 1: Use the batch file (Easiest)
# Double-click this file or run in command prompt:
run_system.bat
Option 2: Manual command
# Navigate to project directory
cd "C:\Users\kunal\Desktop\PEST DETECT"

# Run the system
pest_detect_env\Scripts\python.exe main.py

Option 3: Check status only
# Navigate to project directory
cd "C:\Users\kunal\Desktop\PEST DETECT"

# Check status
pest_detect_env\Scripts\python.exe main.py --status

🌐 Access the System:
Web Dashboard: http://localhost:8000
API Documentation: http://localhost:8000/docs
The system is now fully functional and ready to use! You can start detecting pests, monitoring sensor data, and managing your farm through the web dashboard.


### Running the System

1. **Start the complete system**
   ```bash
   python main.py
   ```

2. **Access the web dashboard**
   Open your browser and go to: `http://localhost:8000`

3. **For single image detection**
   ```bash
   python main.py --detect path/to/image.jpg
   ```

4. **Check system status**
   ```bash
   python main.py --status
   ```

## 🔧 Configuration

Edit `config.json` to customize the system:

- **AI Model**: Adjust confidence thresholds and model parameters
- **IoT System**: Configure GPIO pins and sensor settings
- **Web Dashboard**: Set host, port, and CORS settings
- **Detection**: Configure auto-detection intervals and camera settings

## 📊 Web Dashboard

The web dashboard provides:

- **Real-time Monitoring**: Live system status and sensor data
- **Pest Detection**: Upload images for AI-powered pest detection
- **Statistics**: Comprehensive analytics and trend visualization
- **System Control**: Manual control of IoT devices and actuators

### Dashboard Features

- 📈 **Analytics**: Pest detection trends and statistics
- 🖼️ **Image Upload**: Drag-and-drop pest detection
- 📊 **Charts**: Visual representation of data
- ⚙️ **System Control**: IoT device management
- 📱 **Responsive Design**: Works on desktop and mobile

## 🤖 AI Model

### Supported Pest Types

- Aphid
- Whitefly
- Thrips
- Mite
- Caterpillar
- Beetle
- Grasshopper
- Leafhopper
- Scale Insect
- Mealybug

### Training Your Own Model

1. **Prepare your dataset**
   ```bash
   # Organize images in YOLO format
   dataset/
   ├── train/
   │   ├── images/
   │   └── labels/
   ├── val/
   │   ├── images/
   │   └── labels/
   └── test/
       ├── images/
       └── labels/
   ```

2. **Train the model**
   ```bash
   python ai_model/train.py
   ```

3. **The trained model will be saved as `ai_model/best.pt`**

## 🔌 IoT Integration

### Hardware Requirements

- **Raspberry Pi** (recommended)
- **Relay modules** for actuator control
- **Sensors**: Temperature, humidity, soil moisture, light
- **Motors**: Stepper/servo for camera positioning
- **Camera**: USB camera or Pi Camera

### GPIO Configuration

Configure GPIO pins in `config.json`:

```json
{
  "iot_system": {
    "relay_pins": [18, 19, 20, 21],
    "motor_pins": {
      "stepper": [14, 15, 16, 17],
      "servo": 12
    },
    "sensors": {
      "temperature": {"pin": 4},
      "humidity": {"pin": 17},
      "soil_moisture": {"pin": 27},
      "light": {"pin": 22}
    }
  }
}
```

## 📡 API Endpoints

### Detection
- `POST /detect` - Upload image for pest detection
- `GET /detections` - Get detection history

### System Status
- `GET /system/status` - Get system status
- `POST /system/action` - Trigger system action
- `GET /sensors` - Get sensor data

### Statistics
- `GET /statistics` - Get detection statistics

### WebSocket
- `WS /ws` - Real-time updates

## 🛠️ Development

### Project Structure

- **AI Model**: YOLO-based pest detection
- **IoT Controller**: Hardware abstraction layer
- **Web Dashboard**: React frontend + FastAPI backend
- **Main Orchestrator**: Coordinates all components

### Adding New Features

1. **New Pest Types**: Update class names in detection scripts
2. **New Sensors**: Add sensor configuration and reading logic
3. **New Actuators**: Extend the actuator controller
4. **New API Endpoints**: Add to FastAPI backend

## 🐛 Troubleshooting

### Common Issues

1. **Model not found**: Ensure `ai_model/best.pt` exists
2. **GPIO errors**: Check Raspberry Pi setup and permissions
3. **Camera not detected**: Verify camera connection and permissions
4. **Web dashboard not loading**: Check if React build completed successfully

### Logs

Check `pest_detection.log` for detailed system logs.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📞 Support

For support and questions:
- Create an issue on GitHub
- Check the documentation
- Review the logs for error details

## 🔮 Future Enhancements

- [ ] Mobile app integration
- [ ] Cloud deployment options
- [ ] Advanced analytics and ML insights
- [ ] Multi-camera support
- [ ] Weather integration
- [ ] Automated reporting
- [ ] Integration with farm management systems

---

**Note**: This system is designed for educational and research purposes. For production use in commercial farming, ensure proper testing and validation of pest detection accuracy.
