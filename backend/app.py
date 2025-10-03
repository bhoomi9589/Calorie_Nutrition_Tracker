from flask import Flask, request, jsonify, send_from_directory, send_file
from flask_cors import CORS
import requests
import os
import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get Spoonacular API key from environment variable with fallback
SPOONACULAR_API_KEY = os.getenv('SPOONACULAR_API_KEY') or '14ed33f55842459298f8a6548333a21c'
SPOONACULAR_BASE_URL = 'https://api.spoonacular.com'

# For production deployment, serve React static files
static_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'frontend', 'build')
app = Flask(__name__, static_folder=static_folder, static_url_path='')

print(f"Static folder path: {static_folder}")
print(f"Static folder exists: {os.path.exists(static_folder)}")
if os.path.exists(static_folder):
    print(f"Files in static folder: {os.listdir(static_folder)}")
    # Check if static/js directory exists
    js_folder = os.path.join(static_folder, 'static', 'js')
    if os.path.exists(js_folder):
        print(f"JS files in static/js: {os.listdir(js_folder)}")
    else:
        print("static/js directory does not exist!")
else:
    # Try alternative path for production deployment
    alternative_static = os.path.join(os.getcwd(), 'frontend', 'build')
    print(f"Trying alternative path: {alternative_static}")
    if os.path.exists(alternative_static):
        app.static_folder = alternative_static
        print(f"Using alternative static folder: {alternative_static}")
    else:
        print("No static folder found - frontend may not be available")

# Configure CORS for production
if os.environ.get('FLASK_ENV') == 'production':
    CORS(app, resources={r"/api/*": {"origins": "*"}})
else:
    CORS(app, resources={
        r"/api/*": {
            "origins": ["http://localhost:3000"],
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type"]
        }
    })

# Temporary storage for food logs (replace with database in production)
daily_food_log = []

# Indian foods database for fallback when Spoonacular API doesn't have results
INDIAN_FOODS_DB = {
    # South Indian Breakfast & Snacks
    'dosa': {
        'id': 'indian_dosa_001',
        'title': 'Plain Dosa',
        'image': 'https://images.unsplash.com/photo-1630409351151-b80b322c3d43?w=300&q=80',
        'nutrition': {'calories': 168, 'protein': 4, 'fat': 3, 'carbs': 32}
    },
    'masala dosa': {
        'id': 'indian_masala_dosa_001',
        'title': 'Masala Dosa',
        'image': 'https://images.unsplash.com/photo-1668236543090-82eba5ee5976?w=300&q=80',
        'nutrition': {'calories': 285, 'protein': 6, 'fat': 8, 'carbs': 48}
    },
    'rava dosa': {
        'id': 'indian_rava_dosa_001',
        'title': 'Rava Dosa',
        'image': 'https://images.unsplash.com/photo-1630409351072-b80b322c3d43?w=300&q=80',
        'nutrition': {'calories': 195, 'protein': 5, 'fat': 4, 'carbs': 36}
    },
    'idli': {
        'id': 'indian_idli_001',
        'title': 'Idli (2 pieces)',
        'image': 'https://images.unsplash.com/photo-1546833999-b9f581a1996d?w=300&q=80',
        'nutrition': {'calories': 78, 'protein': 3, 'fat': 1, 'carbs': 16}
    },
    'uttapam': {
        'id': 'indian_uttapam_001',
        'title': 'Vegetable Uttapam',
        'image': 'https://images.unsplash.com/photo-1630409351121-19762d6e3c5d?w=300&q=80',
        'nutrition': {'calories': 195, 'protein': 5, 'fat': 4, 'carbs': 35}
    },
    'medu vada': {
        'id': 'indian_medu_vada_001',
        'title': 'Medu Vada (2 pieces)',
        'image': 'https://images.unsplash.com/photo-1630409351134-b80b322c3d43?w=300&q=80',
        'nutrition': {'calories': 185, 'protein': 6, 'fat': 8, 'carbs': 24}
    },
    'rava idli': {
        'id': 'indian_rava_idli_001',
        'title': 'Rava Idli (2 pieces)',
        'image': 'https://images.unsplash.com/photo-1626074353765-517a681e40be?w=300&q=80',
        'nutrition': {'calories': 95, 'protein': 3, 'fat': 2, 'carbs': 18}
    },
    'appam': {
        'id': 'indian_appam_001',
        'title': 'Appam (2 pieces)',
        'image': 'https://images.unsplash.com/photo-1630409351072-b80b322c3d43?w=300&q=80',
        'nutrition': {'calories': 120, 'protein': 2, 'fat': 1, 'carbs': 26}
    },
    
    # North Indian Street Food & Snacks
    'samosa': {
        'id': 'indian_samosa_001',
        'title': 'Vegetable Samosa',
        'image': 'https://images.unsplash.com/photo-1601050690117-94f5f6fa7fa8?w=300&q=80',
        'nutrition': {'calories': 262, 'protein': 4, 'fat': 17, 'carbs': 24}
    },
    'kachori': {
        'id': 'indian_kachori_001',
        'title': 'Dal Kachori',
        'image': 'https://images.unsplash.com/photo-1666286332363-5caa95e25b60?w=300&q=80',
        'nutrition': {'calories': 186, 'protein': 5, 'fat': 8, 'carbs': 25}
    },
    'aloo tikki': {
        'id': 'indian_aloo_tikki_001',
        'title': 'Aloo Tikki',
        'image': 'https://images.unsplash.com/photo-1606491956689-2ea866880c84?w=300&q=80',
        'nutrition': {'calories': 165, 'protein': 3, 'fat': 7, 'carbs': 24}
    },
    'bhel puri': {
        'id': 'indian_bhel_puri_001',
        'title': 'Bhel Puri',
        'image': 'https://images.unsplash.com/photo-1626074353765-517a681e40be?w=300&q=80',
        'nutrition': {'calories': 220, 'protein': 6, 'fat': 8, 'carbs': 32}
    },
    'sev puri': {
        'id': 'indian_sev_puri_001',
        'title': 'Sev Puri',
        'image': 'https://images.unsplash.com/photo-1601050690117-94f5f6fa7fa8?w=300&q=80',
        'nutrition': {'calories': 180, 'protein': 4, 'fat': 8, 'carbs': 24}
    },
    'pani puri': {
        'id': 'indian_pani_puri_001',
        'title': 'Pani Puri (6 pieces)',
        'image': 'https://images.unsplash.com/photo-1606491956689-2ea866880c84?w=300&q=80',
        'nutrition': {'calories': 120, 'protein': 3, 'fat': 2, 'carbs': 24}
    },
    'dahi puri': {
        'id': 'indian_dahi_puri_001',
        'title': 'Dahi Puri',
        'image': 'https://images.unsplash.com/photo-1601050690117-94f5f6fa7fa8?w=300&q=80',
        'nutrition': {'calories': 150, 'protein': 4, 'fat': 5, 'carbs': 23}
    },
    'pav bhaji': {
        'id': 'indian_pav_bhaji_001',
        'title': 'Pav Bhaji',
        'image': 'https://images.unsplash.com/photo-1606471679504-b6894fe3ad38?w=300&q=80',
        'nutrition': {'calories': 400, 'protein': 12, 'fat': 18, 'carbs': 52}
    },
    'vada pav': {
        'id': 'indian_vada_pav_001',
        'title': 'Vada Pav',
        'image': 'https://images.unsplash.com/photo-1606491956689-2ea866880c84?w=300&q=80',
        'nutrition': {'calories': 290, 'protein': 7, 'fat': 12, 'carbs': 40}
    },
    'misal pav': {
        'id': 'indian_misal_pav_001',
        'title': 'Misal Pav',
        'image': 'https://images.unsplash.com/photo-1626074353765-517a681e40be?w=300&q=80',
        'nutrition': {'calories': 320, 'protein': 12, 'fat': 14, 'carbs': 42}
    },
    
    # Gujarati & Western Indian
    'dhokla': {
        'id': 'indian_dhokla_001',
        'title': 'Dhokla (4 pieces)',
        'image': 'https://images.unsplash.com/photo-1601050690117-94f5f6fa7fa8?w=300&q=80',
        'nutrition': {'calories': 160, 'protein': 6, 'fat': 3, 'carbs': 28}
    },
    'khandvi': {
        'id': 'indian_khandvi_001',
        'title': 'Khandvi',
        'image': 'https://images.unsplash.com/photo-1606491956689-2ea866880c84?w=300&q=80',
        'nutrition': {'calories': 140, 'protein': 5, 'fat': 4, 'carbs': 22}
    },
    'thepla': {
        'id': 'indian_thepla_001',
        'title': 'Thepla (2 pieces)',
        'image': 'https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=300&q=80',
        'nutrition': {'calories': 180, 'protein': 5, 'fat': 6, 'carbs': 28}
    },
    'fafda': {
        'id': 'indian_fafda_001',
        'title': 'Fafda with Jalebi',
        'image': 'https://images.unsplash.com/photo-1599599810769-bcde5a160d32?w=300&q=80',
        'nutrition': {'calories': 280, 'protein': 6, 'fat': 12, 'carbs': 38}
    },
    
    # Breakfast Items
    'poha': {
        'id': 'indian_poha_001',
        'title': 'Poha',
        'image': 'https://images.unsplash.com/photo-1565958011703-44f9829ba187?w=300&q=80',
        'nutrition': {'calories': 180, 'protein': 4, 'fat': 6, 'carbs': 28}
    },
    'upma': {
        'id': 'indian_upma_001',
        'title': 'Upma',
        'image': 'https://images.unsplash.com/photo-1565958011713-44f9829ba187?w=300&q=80',
        'nutrition': {'calories': 200, 'protein': 5, 'fat': 7, 'carbs': 30}
    },
    'aloo paratha': {
        'id': 'indian_aloo_paratha_001',
        'title': 'Aloo Paratha',
        'image': 'https://images.unsplash.com/photo-1596797038530-2c107229654b?w=300&q=80',
        'nutrition': {'calories': 320, 'protein': 8, 'fat': 12, 'carbs': 46}
    },
    'gobi paratha': {
        'id': 'indian_gobi_paratha_001',
        'title': 'Gobi Paratha',
        'image': 'https://images.unsplash.com/photo-1596797038530-2c107229654b?w=300&q=80',
        'nutrition': {'calories': 295, 'protein': 7, 'fat': 11, 'carbs': 42}
    },
    'paneer paratha': {
        'id': 'indian_paneer_paratha_001',
        'title': 'Paneer Paratha',
        'image': 'https://images.unsplash.com/photo-1596797038530-2c107229654b?w=300&q=80',
        'nutrition': {'calories': 350, 'protein': 12, 'fat': 15, 'carbs': 44}
    },
    'methi paratha': {
        'id': 'indian_methi_paratha_001',
        'title': 'Methi Paratha',
        'image': 'https://images.unsplash.com/photo-1596797038530-2c107229654b?w=300&q=80',
        'nutrition': {'calories': 280, 'protein': 8, 'fat': 10, 'carbs': 40}
    },
    
    # Main Courses & Rice Dishes
    'biryani': {
        'id': 'indian_biryani_001',
        'title': 'Vegetable Biryani',
        'image': 'https://images.unsplash.com/photo-1563379091339-03246963d61a?w=300&q=80',
        'nutrition': {'calories': 420, 'protein': 12, 'fat': 15, 'carbs': 62}
    },
    'pulao': {
        'id': 'indian_pulao_001',
        'title': 'Vegetable Pulao',
        'image': 'https://images.unsplash.com/photo-1563379091359-03246963d61a?w=300&q=80',
        'nutrition': {'calories': 320, 'protein': 8, 'fat': 10, 'carbs': 52}
    },
    'jeera rice': {
        'id': 'indian_jeera_rice_001',
        'title': 'Jeera Rice',
        'image': 'https://images.unsplash.com/photo-1563379091369-03246963d61a?w=300&q=80',
        'nutrition': {'calories': 280, 'protein': 6, 'fat': 8, 'carbs': 48}
    },
    
    # Dal & Curry Dishes
    'dal rice': {
        'id': 'indian_dal_rice_001',
        'title': 'Dal Rice',
        'image': 'https://images.unsplash.com/photo-1505253716362-afaea1d3d1af?w=300&q=80',
        'nutrition': {'calories': 290, 'protein': 12, 'fat': 4, 'carbs': 52}
    },
    'rajma': {
        'id': 'indian_rajma_001',
        'title': 'Rajma Rice',
        'image': 'https://images.unsplash.com/photo-1505253716362-afaea1d3d1af?w=300&q=80',
        'nutrition': {'calories': 350, 'protein': 14, 'fat': 8, 'carbs': 58}
    },
    'chole bhature': {
        'id': 'indian_chole_bhature_001',
        'title': 'Chole Bhature',
        'image': 'https://images.unsplash.com/photo-1505253716362-afaea1d3d1af?w=300&q=80',
        'nutrition': {'calories': 485, 'protein': 16, 'fat': 22, 'carbs': 58}
    },
    'dal makhani': {
        'id': 'indian_dal_makhani_001',
        'title': 'Dal Makhani',
        'image': 'https://images.unsplash.com/photo-1505253716362-afaea1d3d1af?w=300&q=80',
        'nutrition': {'calories': 280, 'protein': 12, 'fat': 12, 'carbs': 32}
    },
    'paneer butter masala': {
        'id': 'indian_paneer_butter_masala_001',
        'title': 'Paneer Butter Masala',
        'image': 'https://images.unsplash.com/photo-1631452180519-c014fe946bc7?w=300&q=80',
        'nutrition': {'calories': 320, 'protein': 15, 'fat': 18, 'carbs': 25}
    },
    'palak paneer': {
        'id': 'indian_palak_paneer_001',
        'title': 'Palak Paneer',
        'image': 'https://images.unsplash.com/photo-1631452180529-c014fe946bc7?w=300&q=80',
        'nutrition': {'calories': 285, 'protein': 14, 'fat': 16, 'carbs': 22}
    },
    'kadhi pakora': {
        'id': 'indian_kadhi_pakora_001',
        'title': 'Kadhi Pakora',
        'image': 'https://images.unsplash.com/photo-1505253716362-afaea1d3d1af?w=300&q=80',
        'nutrition': {'calories': 250, 'protein': 8, 'fat': 12, 'carbs': 28}
    },
    
    # Bread Items
    'roti': {
        'id': 'indian_roti_001',
        'title': 'Roti (2 pieces)',
        'image': 'https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=300&q=80',
        'nutrition': {'calories': 140, 'protein': 4, 'fat': 1, 'carbs': 28}
    },
    'naan': {
        'id': 'indian_naan_001',
        'title': 'Plain Naan',
        'image': 'https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=300&q=80',
        'nutrition': {'calories': 285, 'protein': 8, 'fat': 9, 'carbs': 42}
    },
    'butter naan': {
        'id': 'indian_butter_naan_001',
        'title': 'Butter Naan',
        'image': 'https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=300&q=80',
        'nutrition': {'calories': 320, 'protein': 8, 'fat': 12, 'carbs': 42}
    },
    'garlic naan': {
        'id': 'indian_garlic_naan_001',
        'title': 'Garlic Naan',
        'image': 'https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=300&q=80',
        'nutrition': {'calories': 295, 'protein': 8, 'fat': 10, 'carbs': 42}
    },
    'puri': {
        'id': 'indian_puri_001',
        'title': 'Puri (4 pieces)',
        'image': 'https://images.unsplash.com/photo-1599938870781-b5c6f8c5a3bb?w=300&q=80',
        'nutrition': {'calories': 340, 'protein': 8, 'fat': 14, 'carbs': 48}
    },
    'bhatura': {
        'id': 'indian_bhatura_001',
        'title': 'Bhatura (1 piece)',
        'image': 'https://images.unsplash.com/photo-1599938870791-b5c6f8c5a3bb?w=300&q=80',
        'nutrition': {'calories': 280, 'protein': 6, 'fat': 12, 'carbs': 38}
    },
    
    # Sweets & Desserts
    'jalebi': {
        'id': 'indian_jalebi_001',
        'title': 'Jalebi',
        'image': 'https://images.unsplash.com/photo-1599599810769-bcde5a160d32?w=300&q=80',
        'nutrition': {'calories': 150, 'protein': 1, 'fat': 4, 'carbs': 28}
    },
    'imarti': {
        'id': 'indian_imarti_001',
        'title': 'Imarti',
        'image': 'https://images.unsplash.com/photo-1678031487094-8b4fb3b1c0a0?w=300&q=80',
        'nutrition': {'calories': 165, 'protein': 2, 'fat': 5, 'carbs': 30}
    },
    'gulab jamun': {
        'id': 'indian_gulab_jamun_001',
        'title': 'Gulab Jamun (2 pieces)',
        'image': 'https://images.unsplash.com/photo-1594736797933-d0901ba2fe65?w=300&q=80',
        'nutrition': {'calories': 195, 'protein': 3, 'fat': 8, 'carbs': 30}
    },
    'rasgulla': {
        'id': 'indian_rasgulla_001',
        'title': 'Rasgulla (2 pieces)',
        'image': 'https://images.unsplash.com/photo-1594736797963-d0901ba2fe65?w=300&q=80',
        'nutrition': {'calories': 106, 'protein': 4, 'fat': 1, 'carbs': 22}
    },
    'rasmalai': {
        'id': 'indian_rasmalai_001',
        'title': 'Rasmalai (2 pieces)',
        'image': 'https://images.unsplash.com/photo-1594736797973-d0901ba2fe65?w=300&q=80',
        'nutrition': {'calories': 180, 'protein': 6, 'fat': 8, 'carbs': 22}
    },
    'kheer': {
        'id': 'indian_kheer_001',
        'title': 'Rice Kheer',
        'image': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=300&q=80',
        'nutrition': {'calories': 165, 'protein': 4, 'fat': 5, 'carbs': 26}
    },
    'kulfi': {
        'id': 'indian_kulfi_001',
        'title': 'Kulfi',
        'image': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=300&q=80',
        'nutrition': {'calories': 155, 'protein': 4, 'fat': 6, 'carbs': 22}
    },
    'halwa': {
        'id': 'indian_halwa_001',
        'title': 'Carrot Halwa',
        'image': 'https://images.unsplash.com/photo-1578662996452-48f60103fc96?w=300&q=80',
        'nutrition': {'calories': 210, 'protein': 4, 'fat': 8, 'carbs': 32}
    },
    'laddu': {
        'id': 'indian_laddu_001',
        'title': 'Besan Laddu',
        'image': 'https://images.unsplash.com/photo-1594736797943-d0901ba2fe65?w=300&q=80',
        'nutrition': {'calories': 185, 'protein': 4, 'fat': 7, 'carbs': 28}
    },
    'barfi': {
        'id': 'indian_barfi_001',
        'title': 'Kaju Barfi',
        'image': 'https://images.unsplash.com/photo-1594736797953-d0901ba2fe65?w=300&q=80',
        'nutrition': {'calories': 165, 'protein': 3, 'fat': 8, 'carbs': 20}
    },
    
    # Beverages
    'lassi': {
        'id': 'indian_lassi_001',
        'title': 'Sweet Lassi',
        'image': 'https://images.unsplash.com/photo-1595473896097-24b58ddfdc6b?w=300&q=80',
        'nutrition': {'calories': 180, 'protein': 6, 'fat': 4, 'carbs': 32}
    },
    'mango lassi': {
        'id': 'indian_mango_lassi_001',
        'title': 'Mango Lassi',
        'image': 'https://images.unsplash.com/photo-1595473896107-24b58ddfdc6b?w=300&q=80',
        'nutrition': {'calories': 220, 'protein': 6, 'fat': 4, 'carbs': 42}
    },
    'chai': {
        'id': 'indian_chai_001',
        'title': 'Masala Chai',
        'image': 'https://images.unsplash.com/photo-1571934811356-5cc061b6821f?w=300&q=80',
        'nutrition': {'calories': 80, 'protein': 3, 'fat': 3, 'carbs': 12}
    },
    'filter coffee': {
        'id': 'indian_filter_coffee_001',
        'title': 'South Indian Filter Coffee',
        'image': 'https://images.unsplash.com/photo-1509042239860-f550ce710b93?w=300&q=80',
        'nutrition': {'calories': 75, 'protein': 3, 'fat': 3, 'carbs': 10}
    },
    'nimbu pani': {
        'id': 'indian_nimbu_pani_001',
        'title': 'Nimbu Pani (Lemonade)',
        'image': 'https://images.unsplash.com/photo-1595473896117-24b58ddfdc6b?w=300&q=80',
        'nutrition': {'calories': 60, 'protein': 0, 'fat': 0, 'carbs': 15}
    },
    'sugarcane juice': {
        'id': 'indian_sugarcane_juice_001',
        'title': 'Fresh Sugarcane Juice',
        'image': 'https://images.unsplash.com/photo-1595473896127-24b58ddfdc6b?w=300&q=80',
        'nutrition': {'calories': 180, 'protein': 0, 'fat': 0, 'carbs': 45}
    }
}

def search_indian_foods(query):
    """Search for Indian foods in our local database"""
    query_lower = query.lower().strip()
    results = []
    
    for food_key, food_data in INDIAN_FOODS_DB.items():
        # Check if query matches food name (exact or partial)
        if query_lower in food_key or food_key in query_lower:
            results.append(food_data)
        # Also check if query matches in title
        elif query_lower in food_data['title'].lower():
            results.append(food_data)
    
    return results[:10]  # Limit to 10 results

@app.route('/api/search')
def search_food():
    query = request.args.get('query', '')
    if not query:
        return jsonify({'error': 'Query parameter is required'}), 400
    
    try:
        print(f"Searching for query: {query}")
        print(f"Using API key: {SPOONACULAR_API_KEY}")
        
        # First, search Spoonacular API
        response = requests.get(
            f'{SPOONACULAR_BASE_URL}/recipes/complexSearch',
            params={
                'apiKey': SPOONACULAR_API_KEY,
                'query': query,
                'number': 10,  # Limit results to 10 items
                'addNutrition': True
            }
        )
        
        print(f"API Response Status: {response.status_code}")
        spoonacular_results = []
        
        if response.status_code == 200:
            data = response.json()
            print(f"API Response Data: {data}")
            
            if 'results' in data and data['results']:
                spoonacular_results = [{
                    'id': item['id'],
                    'title': item['title'],
                    'image': item['image'],
                    'nutrition': {
                        'calories': item.get('nutrition', {}).get('nutrients', [{'amount': 0}])[0]['amount'],
                        'protein': next((n['amount'] for n in item.get('nutrition', {}).get('nutrients', []) if n['name'] == 'Protein'), 0),
                        'fat': next((n['amount'] for n in item.get('nutrition', {}).get('nutrients', []) if n['name'] == 'Fat'), 0),
                        'carbs': next((n['amount'] for n in item.get('nutrition', {}).get('nutrients', []) if n['name'] == 'Carbohydrates'), 0)
                    }
                } for item in data['results']]
        
        # Search Indian foods database
        indian_results = search_indian_foods(query)
        
        # Combine results - prioritize Spoonacular, then add Indian foods
        combined_results = spoonacular_results + indian_results
        
        # If no results from either source, provide helpful message
        if not combined_results:
            return jsonify({
                'searchResults': [],
                'message': f'No results found for "{query}". Try searching for popular foods like "dosa", "samosa", "biryani", "pizza", "burger", etc.'
            }), 200
        
        # Limit total results to 10
        final_results = combined_results[:10]
        
        return jsonify({
            'searchResults': final_results,
            'message': f'Found {len(final_results)} results for "{query}"'
        })
        
    except Exception as e:
        print(f"Error in search: {str(e)}")
        # If API fails, return only Indian foods results
        indian_results = search_indian_foods(query)
        if indian_results:
            return jsonify({
                'searchResults': indian_results,
                'message': f'Found {len(indian_results)} local results for "{query}"'
            })
        
        return jsonify({
            'error': 'Search service temporarily unavailable',
            'searchResults': [],
            'message': 'Please try again later or search for Indian foods like "dosa", "samosa", "biryani"'
        }), 500
    except requests.RequestException as e:
        print(f"Request Exception: {str(e)}")
        return jsonify({
            'error': 'Failed to fetch data from Spoonacular API',
            'details': str(e)
        }), 500
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return jsonify({
            'error': 'An unexpected error occurred',
            'details': str(e)
        }), 500

@app.route('/api/nutrition')
def get_nutrition():
    food_id = request.args.get('id')
    if not food_id:
        return jsonify({'error': 'Food ID is required'}), 400
    
    try:
        # Check if it's an Indian food from our local database
        if str(food_id).startswith('indian_'):
            # Find the food in our database
            for food_key, food_data in INDIAN_FOODS_DB.items():
                if food_data['id'] == food_id:
                    return jsonify({
                        'nutrition': food_data['nutrition']
                    })
            
            return jsonify({'error': 'Indian food not found in database'}), 404
        
        # For Spoonacular API foods
        response = requests.get(
            f'{SPOONACULAR_BASE_URL}/recipes/{food_id}/information',
            params={
                'apiKey': SPOONACULAR_API_KEY,
                'includeNutrition': True
            }
        )
        response.raise_for_status()
        data = response.json()
        # Transform the response to match frontend expectations
        nutrition_info = {
            'nutrition': {
                'calories': data['nutrition']['nutrients'][0]['amount'],
                'protein': next((n['amount'] for n in data['nutrition']['nutrients'] if n['name'] == 'Protein'), 0),
                'fat': next((n['amount'] for n in data['nutrition']['nutrients'] if n['name'] == 'Fat'), 0),
                'carbs': next((n['amount'] for n in data['nutrition']['nutrients'] if n['name'] == 'Carbohydrates'), 0)
            }
        }
        return jsonify(nutrition_info)
    except requests.RequestException as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/log-food', methods=['POST'])
def log_food():
    food_data = request.json
    if not food_data:
        return jsonify({'error': 'Food data is required'}), 400
    
    # Add timestamp to the food log
    food_entry = {
        **food_data,
        'timestamp': datetime.datetime.now().isoformat()
    }
    daily_food_log.append(food_entry)
    
    return jsonify({
        'message': 'Food logged successfully',
        'food': food_entry
    })

@app.route('/api/daily-log', methods=['GET'])
def get_daily_log():
    return jsonify(daily_food_log)

@app.route('/api/test')
def test_api():
    return jsonify({
        'message': 'Backend is working!',
        'static_folder': app.static_folder,
        'static_folder_exists': os.path.exists(app.static_folder),
        'build_files': os.listdir(app.static_folder) if os.path.exists(app.static_folder) else []
    })

# Explicit static file serving routes
@app.route('/static/<path:filename>')
def serve_static_files(filename):
    try:
        static_path = os.path.join(app.static_folder, 'static')
        print(f"Serving static file: {filename} from {static_path}")
        return send_from_directory(static_path, filename)
    except Exception as e:
        print(f"Error serving static file: {str(e)}")
        return jsonify({'error': f'Static file error: {str(e)}'}), 404

# Serve React App for production deployment
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_react_app(path):
    try:
        print(f"Requested path: {path}")
        print(f"Static folder: {app.static_folder}")
        
        if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
            print(f"Serving file: {path}")
            return send_from_directory(app.static_folder, path)
        else:
            print("Serving index.html")
            index_path = os.path.join(app.static_folder, 'index.html')
            print(f"Index.html exists: {os.path.exists(index_path)}")
            return send_from_directory(app.static_folder, 'index.html')
    except Exception as e:
        print(f"Error serving file: {str(e)}")
        return jsonify({'error': f'File serving error: {str(e)}'}), 500

if __name__ == '__main__':
    if not SPOONACULAR_API_KEY:
        print("Warning: SPOONACULAR_API_KEY environment variable is not set!")
    
    # Use environment variables for production
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_ENV') != 'production'
    
    app.run(host='0.0.0.0', port=port, debug=debug_mode)