# 🚨 RENDER ENVIRONMENT VARIABLES SETUP

## CRITICAL: You MUST set these environment variables in Render Dashboard

### Go to your Render dashboard:
1. Visit: https://dashboard.render.com
2. Click on your service: `calorie-nutrition-tracker-d2r9`
3. Go to "Environment" tab
4. Add these 3 environment variables:

### Required Environment Variables:

| Key | Value | Description |
|-----|-------|-------------|
| `SPOONACULAR_API_KEY` | `14ed33f55842459298f8a6548333a21c` | Your Spoonacular API key |
| `FLASK_ENV` | `production` | Sets Flask to production mode |
| `PORT` | `10000` | Port for Render deployment |

### How to Add Environment Variables in Render:
1. Click "Environment" in the left sidebar
2. Click "Add Environment Variable"
3. Enter Key and Value for each variable above
4. Click "Save Changes"
5. Your service will automatically redeploy

### Expected Result After Setting Variables:
- ✅ No more "SPOONACULAR_API_KEY environment variable is not set!" warning
- ✅ API calls will work properly
- ✅ Production mode enabled (no debug mode)
- ✅ Frontend files should be served correctly

### Check Deployment Status:
After setting environment variables, check the live tail for:
- "Static folder exists: True"
- No API key warnings
- Successful file serving (200 responses instead of 404/500)

## 🎯 Your app should be fully functional after completing these steps!