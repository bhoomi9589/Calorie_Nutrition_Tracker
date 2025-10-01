from flask import Flask, request, jsonify, send_from_directory, send_file
from flask_cors import CORS
import requests
import os
import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# For production deployment, serve React static files
static_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'frontend', 'build')
app = Flask(__name__, static_folder=static_folder, static_url_path='')

print(f"Static folder path: {static_folder}")
print(f"Static folder exists: {os.path.exists(static_folder)}")
if os.path.exists(static_folder):
    print(f"Files in static folder: {os.listdir(static_folder)}")
else:
    # Try alternative path for production deployment
    alternative_static = os.path.join(os.getcwd(), 'frontend', 'build')
    print(f"Trying alternative path: {alternative_static}")
    if os.path.exists(alternative_static):
        app.static_folder = alternative_static
print(f"Static folder path: {static_folder}")
print(f"Static folder exists: {os.path.exists(static_folder)}")
if os.path.exists(static_folder):
    print(f"Files in static folder: {os.listdir(static_folder)}")
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

# Get Spoonacular API key from environment variable
SPOONACULAR_API_KEY = os.getenv('SPOONACULAR_API_KEY')
SPOONACULAR_BASE_URL = 'https://api.spoonacular.com'

# Temporary storage for food logs (replace with database in production)
daily_food_log = []

@app.route('/api/search')
def search_food():
    query = request.args.get('query', '')
    if not query:
        return jsonify({'error': 'Query parameter is required'}), 400
    
    try:
        print(f"Searching for query: {query}")
        print(f"Using API key: {SPOONACULAR_API_KEY}")
        
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
        if response.status_code != 200:
            print(f"API Error Response: {response.text}")
            return jsonify({'error': 'Error from Spoonacular API', 'details': response.text}), response.status_code
            
        data = response.json()
        print(f"API Response Data: {data}")
        
        if 'results' not in data:
            return jsonify({'searchResults': [], 'message': 'No results found'}), 200
            
        search_results = [{
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
        return jsonify({'searchResults': search_results})
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