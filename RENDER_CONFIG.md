# 🚀 Render Configuration for bhoomi9589/Calorie_Nutrition_Tracker

## Render Web Service Settings:

### Basic Settings:
- **Name**: `nutrition-tracker` (or any name you prefer)
- **Repository**: `bhoomi9589/Calorie_Nutrition_Tracker`
- **Branch**: `main`
- **Root Directory**: (leave blank)
- **Environment**: `Python 3`
- **Region**: Choose closest to you
- **Instance Type**: `Free` (for testing)

### Build & Deploy Settings:
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python backend/app.py`

### Environment Variables (IMPORTANT!):
Click "Advanced" and add these:

| Key | Value |
|-----|-------|
| `SPOONACULAR_API_KEY` | `14ed33f55842459298f8a6548333a21c` |
| `FLASK_ENV` | `production` |
| `PORT` | `10000` |

### Auto-Deploy:
- ✅ Enable "Auto-Deploy" from GitHub

## 🎯 After Configuration:
1. Click "Create Web Service"
2. Wait 5-10 minutes for deployment
3. Your app will be live at: `https://nutrition-tracker.onrender.com`

## 🌟 Your Live App Will Have:
- ✅ Beautiful pastel green theme
- ✅ Food search with Spoonacular API
- ✅ Nutrition tracking and charts
- ✅ Responsive design
- ✅ Production-ready performance