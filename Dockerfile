
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
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
