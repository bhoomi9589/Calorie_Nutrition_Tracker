# 🚀 Heroku Deployment Guide

## Step 1: Install Heroku CLI
Download and install from: https://devcenter.heroku.com/articles/heroku-cli

## Step 2: Login to Heroku
```bash
heroku login
```

## Step 3: Create Heroku App
```bash
heroku create your-nutrition-tracker-name
```

## Step 4: Set Environment Variables
```bash
heroku config:set SPOONACULAR_API_KEY=14ed33f55842459298f8a6548333a21c
heroku config:set FLASK_ENV=production
```

## Step 5: Deploy
```bash
git push heroku main
```

## Step 6: Open Your App
```bash
heroku open
```

Your app will be live at: https://your-nutrition-tracker-name.herokuapp.com