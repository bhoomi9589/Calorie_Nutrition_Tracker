# Calorie & Nutrition Tracker - Deployment Guide

## 🚀 Production Deployment Options

### 1. **Heroku Deployment**

#### Prerequisites:
- Install [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
- Create a Heroku account

#### Steps:
```bash
# 1. Initialize git repository (if not already done)
git init
git add .
git commit -m "Initial commit"

# 2. Create Heroku app
heroku create your-nutrition-tracker-app

# 3. Set environment variables
heroku config:set SPOONACULAR_API_KEY=your_spoonacular_api_key_here
heroku config:set FLASK_ENV=production

# 4. Deploy to Heroku
git push heroku main
```

### 2. **Vercel Deployment**

#### For React Frontend:
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy from frontend directory
cd frontend
vercel --prod
```

#### For Flask Backend:
Create `vercel.json` in root directory and deploy backend separately.

### 3. **Railway Deployment**

#### Steps:
1. Connect your GitHub repository to Railway
2. Set environment variables in Railway dashboard
3. Deploy automatically from GitHub

### 4. **Local Production Server**

#### Steps:
```bash
# Install production dependencies
pip install -r requirements.txt

# Set environment variables
export FLASK_ENV=production
export SPOONACULAR_API_KEY=your_api_key_here

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 backend.app:app
```

## 🔧 Environment Variables Required

- `SPOONACULAR_API_KEY`: Your Spoonacular API key
- `FLASK_ENV`: Set to 'production' for production deployment
- `PORT`: Port number (automatically set by most hosting platforms)

## 📁 Project Structure for Deployment

```
Calorie_Nutrion_Tracker/
├── backend/
│   ├── app.py (Updated for production)
│   └── .env (API keys - DO NOT commit)
├── frontend/
│   ├── build/ (Production React build)
│   ├── src/
│   └── package.json
├── requirements.txt (Python dependencies)
├── Procfile (For Heroku)
├── runtime.txt (Python version)
└── README.md (This file)
```

## ✅ Deployment Checklist

- [x] React app built for production (`npm run build`)
- [x] Flask backend configured to serve static files
- [x] Environment variables configured
- [x] Requirements.txt created
- [x] Procfile created for Heroku
- [x] CORS configured for production
- [x] Debug mode disabled in production

## 🎨 Features

- Beautiful pastel green theme
- Food search with Spoonacular API
- Nutrition tracking and visualization
- Responsive design
- Production-ready deployment

## 🔗 API Endpoints

- `GET /api/search?query=<food_name>` - Search for food items
- `GET /api/nutrition/<recipe_id>` - Get nutrition information
- `POST /api/log-food` - Log food consumption
- `GET /api/daily-log` - Get daily food log

## 📱 Access Your Deployed App

After deployment, your app will be accessible at:
- Heroku: `https://your-app-name.herokuapp.com`
- Vercel: `https://your-app-name.vercel.app`
- Railway: `https://your-app-name.up.railway.app`