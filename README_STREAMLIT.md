# 🐛 Pest Detection System - Streamlit Cloud Deployment

This is a web-based pest detection system built with Streamlit that can be deployed on Streamlit Cloud for free.

## 🌐 Live Demo

Once deployed, your app will be available at:
`https://your-app-name.streamlit.app`

## 🚀 Quick Deploy to Streamlit Cloud

### Step 1: Push to GitHub
1. Create a new repository on GitHub
2. Push this code to your repository
3. Make sure `streamlit_app.py` is in the root directory

### Step 2: Deploy on Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click "New app"
4. Select your repository
5. Set the main file to `streamlit_app.py`
6. Click "Deploy!"

## 📱 Features

### 🏠 Dashboard
- System overview and metrics
- Recent detection history
- Detection trends and charts

### 🔍 Pest Detection
- Image upload interface
- AI-powered pest detection (simulated)
- Real-time results display

### 📊 Analytics
- Pest type distribution
- Confidence analysis
- Time-series trends

### ⚙️ System Status
- IoT sensor data simulation
- System component status
- Real-time monitoring

### 📈 Training Interface
- Model information
- Training options
- Dataset management

## 🛠️ Local Development

To run locally:

```bash
# Install requirements
pip install -r requirements.txt

# Run the app
streamlit run streamlit_app.py
```

## 📁 Project Structure

```
├── streamlit_app.py          # Main Streamlit application
├── requirements.txt          # Python dependencies
├── README_STREAMLIT.md      # This file
├── datasets/                # Dataset structure
│   └── pest_dataset/
│       ├── images/
│       └── labels/
├── ai_model/                # AI model files
│   ├── train.py
│   ├── detect.py
│   └── data.yaml
└── iot_controller/          # IoT controller
    └── actuator.py
```

## 🔧 Configuration

The app uses session state to store:
- Detection history
- System status
- User preferences

## 📊 Demo Data

The app includes simulated data for demonstration:
- Mock pest detections
- Simulated IoT sensor readings
- Sample charts and analytics

## 🎯 Customization

To customize the app:
1. Edit `streamlit_app.py`
2. Modify the UI components
3. Add your own AI model
4. Update the styling

## 🔒 Security

- No personal data is stored
- Images are processed in memory only
- Detection history is session-based

## 📈 Performance

- Optimized for Streamlit Cloud
- Lightweight dependencies
- Efficient data processing
- Responsive design

## 🐛 Troubleshooting

### Common Issues:
1. **App won't start**: Check `requirements.txt`
2. **Import errors**: Ensure all dependencies are listed
3. **Memory issues**: Reduce image sizes
4. **Slow loading**: Check internet connection

### Getting Help:
- Check Streamlit Cloud logs
- Test locally first
- Review the documentation

## 🎉 Next Steps

1. **Deploy your app** to Streamlit Cloud
2. **Test all features** with the demo data
3. **Add your own images** for real testing
4. **Share the link** with others
5. **Collect feedback** and improve

---

**Ready to deploy?** Push to GitHub and deploy on Streamlit Cloud!
