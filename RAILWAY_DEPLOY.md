# 🚂 Railway Deployment Guide

## Step 1: Push to GitHub
1. Create repository on GitHub
2. Push your code: 
   ```bash
   git remote add origin https://github.com/yourusername/nutrition-tracker.git
   git push -u origin main
   ```

## Step 2: Deploy on Railway
1. Go to https://railway.app
2. Sign up with GitHub
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Choose your nutrition-tracker repository
6. Railway will auto-detect it's a Python app
7. Add Environment Variables in Railway dashboard:
   - `SPOONACULAR_API_KEY`: 14ed33f55842459298f8a6548333a21c
   - `FLASK_ENV`: production
8. Deploy automatically happens!

Your app will be live at: https://nutrition-tracker-production.up.railway.app