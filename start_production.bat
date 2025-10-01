@echo off
echo Starting Calorie & Nutrition Tracker in Production Mode...
echo.

REM Set environment variables
set FLASK_ENV=production
set PORT=8000

REM Start the Flask application
E:\internship\Calorie_Nutrion_Tracker\.venv\Scripts\python.exe E:\internship\Calorie_Nutrion_Tracker\backend\app.py

pause