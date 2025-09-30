#!/usr/bin/env python3
"""
Pest Detection Web App - Streamlit Cloud Version (No OpenCV)
A simple web interface for pest detection and monitoring
"""

import streamlit as st
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
        font-size: 2.5rem;
        color: #2E8B57;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #2E8B57;
    }
    .status-online {
        color: #28a745;
        font-weight: bold;
    }
    .status-offline {
        color: #dc3545;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Demo data
DEMO_DATA = {
    "detections": [
        {"pest": "Aphid", "count": 15, "confidence": 0.92,
            "timestamp": "2024-01-15 10:30:00"},
        {"pest": "Whitefly", "count": 8, "confidence": 0.87,
            "timestamp": "2024-01-15 11:15:00"},
        {"pest": "Caterpillar", "count": 3, "confidence": 0.95,
            "timestamp": "2024-01-15 12:00:00"},
        {"pest": "Beetle", "count": 12, "confidence": 0.89,
            "timestamp": "2024-01-15 13:30:00"},
        {"pest": "Mite", "count": 25, "confidence": 0.91,
            "timestamp": "2024-01-15 14:45:00"},
    ],
    "sensor_data": {
        "temperature": 24.5,
        "humidity": 65.2,
        "soil_moisture": 78.3,
        "light_intensity": 850
    },
    "system_status": {
        "ai_model": "Online",
        "iot_controller": "Online",
        "camera": "Online",
        "sensors": "Online"
    }
}


def create_demo_image():
    """Create a demo image for display"""
    # Create a simple demo image using matplotlib
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.text(0.5, 0.5, 'Pest Detection Demo\n\nUpload your own image\nfor real detection',
            ha='center', va='center', fontsize=16,
            bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgreen", alpha=0.7))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    # Convert to PIL Image
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=150, bbox_inches='tight')
    buf.seek(0)
    return Image.open(buf)


def main():
    # Header
    st.markdown('<h1 class="main-header">🐛 Pest Detection System</h1>',
                unsafe_allow_html=True)
    st.markdown("---")

    # Sidebar
    with st.sidebar:
        st.header("🔧 System Controls")

        # System Status
        st.subheader("System Status")
        for component, status in DEMO_DATA["system_status"].items():
            status_class = "status-online" if status == "Online" else "status-offline"
            st.markdown(f"**{component.replace('_', ' ').title()}**: <span class='{status_class}'>{status}</span>",
                        unsafe_allow_html=True)

        st.markdown("---")

        # Detection Settings
        st.subheader("Detection Settings")
        confidence_threshold = st.slider(
            "Confidence Threshold", 0.0, 1.0, 0.8, 0.01)
        detection_interval = st.selectbox(
            "Detection Interval", ["1 minute", "5 minutes", "10 minutes", "30 minutes"])

        st.markdown("---")

        # Quick Actions
        st.subheader("Quick Actions")
        if st.button("🔄 Refresh Data"):
            st.rerun()

        if st.button("📊 Generate Report"):
            st.success("Report generated successfully!")

        if st.button("⚙️ System Settings"):
            st.info("Settings panel would open here")

    # Main content tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["📸 Detection", "📊 Analytics", "🌡️ Environment", "⚙️ System", "📚 Training"])

    with tab1:
        st.header("Pest Detection")

        col1, col2 = st.columns([2, 1])

        with col1:
            st.subheader("Image Upload")
            uploaded_file = st.file_uploader(
                "Choose an image", type=['png', 'jpg', 'jpeg'])

            if uploaded_file is not None:
                image = Image.open(uploaded_file)
                st.image(image, caption="Uploaded Image",
                         use_column_width=True)

                # Simulate detection
                if st.button("🔍 Detect Pests"):
                    with st.spinner("Analyzing image..."):
                        time.sleep(2)  # Simulate processing time

                    # Show demo results
                    st.success("Detection completed!")

                    # Display results
                    results_df = pd.DataFrame(DEMO_DATA["detections"])
                    st.dataframe(results_df, use_container_width=True)
            else:
                # Show demo image
                demo_image = create_demo_image()
                st.image(
                    demo_image, caption="Demo Image - Upload your own for detection", use_column_width=True)

        with col2:
            st.subheader("Recent Detections")
            for detection in DEMO_DATA["detections"][:3]:
                with st.container():
                    st.markdown(f"**{detection['pest']}**")
                    st.markdown(f"Count: {detection['count']}")
                    st.markdown(f"Confidence: {detection['confidence']:.2f}")
                    st.markdown(f"Time: {detection['timestamp']}")
                    st.markdown("---")

    with tab2:
        st.header("Analytics Dashboard")

        # Metrics
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Total Detections", "63", "12%")
        with col2:
            st.metric("Pest Species", "5", "2")
        with col3:
            st.metric("Avg Confidence", "90.8%", "3.2%")
        with col4:
            st.metric("Detection Rate", "85%", "5%")

        # Charts
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Pest Distribution")
            pest_counts = {d['pest']: d['count']
                           for d in DEMO_DATA["detections"]}
            fig = px.pie(values=list(pest_counts.values()),
                         names=list(pest_counts.keys()))
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader("Detection Timeline")
            dates = pd.date_range(start='2024-01-10',
                                  end='2024-01-15', freq='D')
            counts = np.random.randint(5, 20, len(dates))
            timeline_df = pd.DataFrame({'Date': dates, 'Detections': counts})
            fig = px.line(timeline_df, x='Date', y='Detections')
            st.plotly_chart(fig, use_container_width=True)

    with tab3:
        st.header("Environmental Monitoring")

        # Sensor data
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Current Readings")
            sensor_data = DEMO_DATA["sensor_data"]

            st.metric("Temperature",
                      f"{sensor_data['temperature']}°C", "2.1°C")
            st.metric("Humidity", f"{sensor_data['humidity']}%", "5%")
            st.metric("Soil Moisture",
                      f"{sensor_data['soil_moisture']}%", "3%")
            st.metric("Light Intensity",
                      f"{sensor_data['light_intensity']} lux", "50")

        with col2:
            st.subheader("Environmental Chart")
            # Create a simple environmental chart
            metrics = ['Temperature', 'Humidity', 'Soil Moisture', 'Light']
            values = [sensor_data['temperature'], sensor_data['humidity'],
                      sensor_data['soil_moisture'], sensor_data['light_intensity']/10]

            fig = px.bar(x=metrics, y=values, title="Environmental Metrics")
            st.plotly_chart(fig, use_container_width=True)

    with tab4:
        st.header("System Configuration")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("AI Model Settings")
            model_version = st.selectbox(
                "Model Version", ["YOLOv8n", "YOLOv8s", "YOLOv8m", "YOLOv8l"])
            st.text_input("Model Path", value="ai_model/best.pt")
            st.slider("Detection Threshold", 0.0, 1.0, 0.5)
            st.slider("NMS Threshold", 0.0, 1.0, 0.4)

        with col2:
            st.subheader("IoT Controller Settings")
            st.checkbox("Enable Camera", value=True)
            st.checkbox("Enable Sensors", value=True)
            st.checkbox("Enable Actuators", value=True)
            st.number_input("Detection Interval (seconds)",
                            min_value=1, max_value=3600, value=300)

        st.subheader("System Logs")
        log_data = [
            "2024-01-15 14:45:00 - System started successfully",
            "2024-01-15 14:44:30 - AI model loaded",
            "2024-01-15 14:44:15 - Camera initialized",
            "2024-01-15 14:44:00 - Sensors connected",
            "2024-01-15 14:43:45 - IoT controller online"
        ]

        for log in log_data:
            st.text(log)

    with tab5:
        st.header("Model Training")

        st.info("🚧 Training interface would be available in the full version")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Training Configuration")
            st.selectbox("Model Size", [
                         "YOLOv8n", "YOLOv8s", "YOLOv8m", "YOLOv8l", "YOLOv8x"])
            st.number_input("Epochs", min_value=1, max_value=1000, value=100)
            st.number_input("Batch Size", min_value=1, max_value=64, value=16)
            st.selectbox("Device", ["CPU", "GPU"])

        with col2:
            st.subheader("Dataset Information")
            st.metric("Training Images", "1,200")
            st.metric("Validation Images", "300")
            st.metric("Test Images", "150")
            st.metric("Classes", "10")

        if st.button("🚀 Start Training"):
            st.warning(
                "Training would start in the full version with actual data")


if __name__ == "__main__":
    main()
