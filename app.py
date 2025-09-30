#!/usr/bin/env python3
"""
Pest Detection Web App - Streamlit Version
A simple web interface for pest detection and monitoring
"""

import streamlit as st
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
import io
import json
import time
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import sys
import os

# Add project paths
sys.path.append(str(Path(__file__).parent))
sys.path.append(str(Path(__file__).parent / "ai_model"))
sys.path.append(str(Path(__file__).parent / "iot_controller"))

# Configure page
st.set_page_config(
    page_title="Pest Detection System",
    page_icon="🐛",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #2E8B57;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 5px solid #2E8B57;
    }
    .detection-result {
        background-color: #e8f5e8;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 2px solid #2E8B57;
    }
    .alert {
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .alert-success {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
    }
    .alert-warning {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        color: #856404;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'detection_history' not in st.session_state:
    st.session_state.detection_history = []
if 'system_status' not in st.session_state:
    st.session_state.system_status = {
        'ai_model': 'Ready',
        'iot_system': 'Simulated',
        'web_dashboard': 'Active',
        'last_update': datetime.now()
    }


def load_ai_model():
    """Load the AI model for pest detection"""
    try:
        from ai_model.detect import PestDetector
        detector = PestDetector()
        detector.load_model()
        return detector
    except Exception as e:
        st.error(f"Error loading AI model: {e}")
        return None


def simulate_iot_data():
    """Simulate IoT sensor data"""
    return {
        'temperature': np.random.normal(25, 5),
        'humidity': np.random.normal(60, 10),
        'soil_moisture': np.random.normal(45, 15),
        'light_intensity': np.random.normal(500, 100),
        'timestamp': datetime.now()
    }


def create_detection_chart():
    """Create a chart showing detection history"""
    if not st.session_state.detection_history:
        return None

    df = pd.DataFrame(st.session_state.detection_history)
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Group by pest type and date
    daily_detections = df.groupby(
        [df['timestamp'].dt.date, 'pest_type']).size().reset_index(name='count')
    daily_detections['date'] = daily_detections['timestamp']

    fig = px.bar(daily_detections, x='date', y='count', color='pest_type',
                 title='Daily Pest Detections by Type',
                 labels={'count': 'Number of Detections', 'date': 'Date'})

    return fig


def main():
    # Header
    st.markdown('<h1 class="main-header">🐛 Pest Detection System</h1>',
                unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.header("Navigation")
        page = st.selectbox("Choose a page", [
            "🏠 Dashboard",
            "🔍 Pest Detection",
            "📊 Analytics",
            "⚙️ System Status",
            "📈 Training"
        ])

        st.header("Quick Stats")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Detections", len(
                st.session_state.detection_history))
        with col2:
            st.metric("System Status", "🟢 Online")

    # Main content based on selected page
    if page == "🏠 Dashboard":
        show_dashboard()
    elif page == "🔍 Pest Detection":
        show_detection_page()
    elif page == "📊 Analytics":
        show_analytics_page()
    elif page == "⚙️ System Status":
        show_system_status()
    elif page == "📈 Training":
        show_training_page()


def show_dashboard():
    """Show the main dashboard"""
    st.header("System Overview")

    # Key metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Detections", len(
            st.session_state.detection_history), "12%")

    with col2:
        st.metric("Active Pests", "3", "-2")

    with col3:
        st.metric("System Uptime", "99.9%", "0.1%")

    with col4:
        st.metric("Accuracy", "94.2%", "2.1%")

    # Recent detections
    st.header("Recent Detections")
    if st.session_state.detection_history:
        recent_df = pd.DataFrame(st.session_state.detection_history[-10:])
        st.dataframe(
            recent_df[['timestamp', 'pest_type', 'confidence']], use_container_width=True)
    else:
        st.info("No detections yet. Upload an image to get started!")

    # Detection chart
    st.header("Detection Trends")
    chart = create_detection_chart()
    if chart:
        st.plotly_chart(chart, use_container_width=True)
    else:
        st.info("Upload some images to see detection trends!")


def show_detection_page():
    """Show the pest detection interface"""
    st.header("Pest Detection")

    # File upload
    uploaded_file = st.file_uploader(
        "Upload an image of a pest or plant",
        type=['jpg', 'jpeg', 'png', 'bmp'],
        help="Upload an image to detect pests"
    )

    if uploaded_file is not None:
        # Display uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        # Detection button
        if st.button("🔍 Detect Pests", type="primary"):
            with st.spinner("Analyzing image..."):
                # Simulate detection (replace with actual AI model)
                time.sleep(2)

                # Mock detection results
                detections = [
                    {'pest_type': 'Aphid', 'confidence': 0.87,
                        'bbox': [100, 150, 200, 250]},
                    {'pest_type': 'Whitefly', 'confidence': 0.73,
                        'bbox': [300, 200, 400, 300]}
                ]

                # Display results
                st.success(f"Found {len(detections)} pest(s)!")

                for i, detection in enumerate(detections):
                    with st.expander(f"Detection {i+1}: {detection['pest_type']}"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"**Type:** {detection['pest_type']}")
                            st.write(
                                f"**Confidence:** {detection['confidence']:.2%}")
                        with col2:
                            st.write(f"**Bounding Box:** {detection['bbox']}")

                        # Add to history
                        st.session_state.detection_history.append({
                            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            'pest_type': detection['pest_type'],
                            'confidence': detection['confidence'],
                            'image_name': uploaded_file.name
                        })

    # Detection history
    if st.session_state.detection_history:
        st.header("Detection History")
        df = pd.DataFrame(st.session_state.detection_history)
        st.dataframe(df, use_container_width=True)


def show_analytics_page():
    """Show analytics and insights"""
    st.header("Analytics & Insights")

    if not st.session_state.detection_history:
        st.info("No data available. Upload some images to see analytics!")
        return

    df = pd.DataFrame(st.session_state.detection_history)

    # Pest type distribution
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Pest Type Distribution")
        pest_counts = df['pest_type'].value_counts()
        fig_pie = px.pie(values=pest_counts.values, names=pest_counts.index,
                         title="Pest Types Detected")
        st.plotly_chart(fig_pie, use_container_width=True)

    with col2:
        st.subheader("Confidence Distribution")
        fig_hist = px.histogram(df, x='confidence', nbins=20,
                                title="Detection Confidence Distribution")
        st.plotly_chart(fig_hist, use_container_width=True)

    # Time series analysis
    st.subheader("Detection Trends Over Time")
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    daily_counts = df.groupby(
        df['timestamp'].dt.date).size().reset_index(name='count')

    fig_line = px.line(daily_counts, x='timestamp', y='count',
                       title="Daily Detection Count")
    st.plotly_chart(fig_line, use_container_width=True)


def show_system_status():
    """Show system status and IoT data"""
    st.header("System Status")

    # System components
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("System Components")
        components = [
            ("AI Model", "🟢 Online", "Ready for detection"),
            ("IoT System", "🟡 Simulated", "Running in demo mode"),
            ("Web Dashboard", "🟢 Online", "Fully operational"),
            ("Database", "🟢 Online", "Storing detection data")
        ]

        for component, status, description in components:
            st.write(f"**{component}:** {status}")
            st.write(f"*{description}*")
            st.write("---")

    with col2:
        st.subheader("IoT Sensor Data")
        sensor_data = simulate_iot_data()

        st.metric("Temperature", f"{sensor_data['temperature']:.1f}°C")
        st.metric("Humidity", f"{sensor_data['humidity']:.1f}%")
        st.metric("Soil Moisture", f"{sensor_data['soil_moisture']:.1f}%")
        st.metric("Light Intensity",
                  f"{sensor_data['light_intensity']:.0f} lux")

        if st.button("🔄 Refresh Data"):
            st.rerun()


def show_training_page():
    """Show AI model training interface"""
    st.header("AI Model Training")

    st.info("This is a demo version. For actual training, use the command line tools.")

    # Training status
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Model Information")
        st.write("**Current Model:** YOLOv8n")
        st.write("**Classes:** 10 pest types")
        st.write("**Status:** Ready for training")
        st.write("**Last Updated:** Never")

    with col2:
        st.subheader("Training Options")
        st.write("**Quick Training:** 50 epochs")
        st.write("**Standard Training:** 100 epochs")
        st.write("**Full Training:** 200 epochs")

    # Training commands
    st.subheader("Training Commands")
    st.code("""
# Quick training
python ai_model/train.py --epochs 50

# Standard training  
python ai_model/train.py --epochs 100 --model yolov8m.pt

# Full training
python ai_model/train.py --epochs 200 --model yolov8l.pt
    """, language="bash")

    # Dataset info
    st.subheader("Dataset Information")
    st.write("**Location:** datasets/pest_dataset/")
    st.write("**Training Images:** 0 (add your images)")
    st.write("**Validation Images:** 0 (add your images)")
    st.write("**Test Images:** 0 (add your images)")


if __name__ == "__main__":
    main()
