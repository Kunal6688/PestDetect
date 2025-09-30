#!/bin/bash

echo "Starting Pest Detection System..."
echo

# Activate virtual environment
echo "Activating virtual environment..."
source pest_detect_env/bin/activate

# Start the system
echo "Starting the system..."
python main.py
