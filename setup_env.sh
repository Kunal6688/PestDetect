#!/bin/bash

echo "Setting up Pest Detection System Environment..."
echo

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv pest_detect_env

# Activate virtual environment
echo "Activating virtual environment..."
source pest_detect_env/bin/activate

# Upgrade pip
echo "Upgrading pip..."
python -m pip install --upgrade pip

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Install Node.js dependencies for frontend
echo "Installing Node.js dependencies..."
cd web_dashboard/frontend
npm install
cd ../..

# Build React frontend
echo "Building React frontend..."
cd web_dashboard/frontend
npm run build
cd ../..

echo
echo "Environment setup complete!"
echo
echo "To activate the environment in the future, run:"
echo "source pest_detect_env/bin/activate"
echo
echo "To start the system, run:"
echo "python main.py"
echo
