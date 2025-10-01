# 🌐 Render Deployment Guide

## Step 1: Push to GitHub
1. Create a new repository on GitHub
2. Add remote: `git remote add origin https://github.com/yourusername/nutrition-tracker.git`
3. Push: `git push -u origin main`

## Step 2: Deploy on Render
1. Go to https://render.com
2. Sign up/Login with GitHub
3. Click "New +" → "Web Service"
4. Connect your GitHub repository
5. Configure:
   - **Name**: nutrition-tracker
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python backend/app.py`
6. Add Environment Variables:
   - `SPOONACULAR_API_KEY`: 14ed33f55842459298f8a6548333a21c
   - `FLASK_ENV`: production
7. Click "Create Web Service"

Your app will be live at: https://nutrition-tracker.onrender.com