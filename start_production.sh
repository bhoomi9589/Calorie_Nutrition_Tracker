#!/bin/bash
echo "Starting Calorie & Nutrition Tracker in Production Mode..."
echo

# Set environment variables
export FLASK_ENV=production
export PORT=8000

# Start the Flask application
python backend/app.py