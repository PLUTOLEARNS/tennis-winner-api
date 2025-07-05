from flask import Flask, request, jsonify
from flask_cors import CORS
import re
import logging
import csv
import os
import subprocess
import sys
import base64
from typing import Dict, Any, Optional
from functools import wraps

app = Flask(__name__)
CORS(app)
app.config['JSON_SORT_KEYS'] = False
# Load API key and credentials from environment variables
API_KEY = os.getenv("API_KEY")
user = os.getenv("USERNAME")
pwd = os.getenv("PASSWORD")
# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
def require_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check for API key in headers or query parameters
        api_key = request.headers.get('X-API-Key') or request.args.get('api_key')
        if api_key:
            if api_key == API_KEY:
                logger.info("Authentication successful via API key")
                return f(*args, **kwargs)
            else:
                return jsonify({
                    'error': 'Invalid API key',
                    'message': 'The provided API key is invalid'
                }), 403
        # Check for Basic Auth
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Basic '):
            try:
                auth_value = auth_header.split(' ', 1)[1]
                decoded_auth = base64.b64decode(auth_value).decode('utf-8')
                username, password = decoded_auth.split(':', 1)
                
                if username == user and password == pwd:
                    logger.info("Authentication successful via Basic Auth")
                    return f(*args, **kwargs)  # Basic Auth valid
                else:
                    return jsonify({'error': 'Invalid credentials'}), 403
            except Exception as e:
                logger.error(f"Error decoding Basic Auth: {e}")
                return jsonify({'error': 'Invalid auth format'}), 401
        # No valid authentication found
        return jsonify({'error': 'Authentication required'}), 401
    return decorated_function
def ensure_csv_exists():
    csv_file = 'wimbledon_finals.csv'
    extract_script = 'extract_data.py'
    
    if not os.path.exists(csv_file):
        logger.info(f"CSV file {csv_file} not found. Attempting to create it...")
        
        if not os.path.exists(extract_script):
            logger.error(f"Extract script {extract_script} not found. Cannot create CSV file.")
            return False
        
        try:
            logger.info(f"Running {extract_script} to generate CSV data...")
            result = subprocess.run([sys.executable, extract_script], 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=60)
            
            if result.returncode == 0:
                logger.info("Successfully executed extract_data.py")
                if os.path.exists(csv_file):
                    logger.info(f"CSV file {csv_file} created successfully")
                    return True
                else:
                    logger.error(f"extract_data.py ran successfully but {csv_file} was not created")
                    return False
            else:
                logger.error(f"extract_data.py failed with return code {result.returncode}")
                logger.error(f"stderr: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            logger.error("extract_data.py timed out after 60 seconds")
            return False
        except Exception as e:
            logger.error(f"Error running extract_data.py: {e}")
            return False
    
    return True

def load_year_data(target_year: int) -> Optional[Dict[str, Any]]:
    csv_file = 'wimbledon_finals.csv'
    
    # Ensure CSV exists before trying to read it
    if not ensure_csv_exists():
        return None
    
    try:
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                try:
                    year = int(row['year'])
                    
                    # Only process the target year
                    if year == target_year:
                        # Determine if tiebreak occurred
                        tiebreak_value = row.get('tiebreak', '0')
                        has_tiebreak = bool(int(tiebreak_value)) if tiebreak_value.isdigit() else has_tiebreak_in_score(row['score'])
                        
                        return {
                            "champion": row['champion'].strip(),
                            "runner_up": row['runner_up'].strip(),
                            "score": row['score'].strip(),
                            "sets": int(row['sets']),
                            "tiebreak": has_tiebreak
                        }
                        
                except (ValueError, KeyError) as e:
                    logger.warning(f"Error processing row {row}: {e}")
                    continue
        
        # If we get here, the year wasn't found
        return None
        
    except Exception as e:
        logger.error(f"Error loading CSV file: {e}")
        return None

def has_tiebreak_in_score(score: str) -> bool:
    # Look for tiebreak patterns like 7-6(4), 6-7(4-7), etc.
    tiebreak_pattern = r'\d+-\d+\(\d+(-\d+)?\)'
    return bool(re.search(tiebreak_pattern, score))

def validate_year(year_str: str) -> Optional[int]:
    try:
        year = int(year_str)
        if year < 1877 or year > 2024:
            return None
        return year
    except (ValueError, TypeError):
        return None

def format_score(score: str) -> str:
    # Normalize all dash characters to regular hyphens for better JSON readability
    return score.replace('–', '-').replace('—', '-').replace('â€"', '-')

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "message": "Wimbledon API is running"
    }), 200

@app.route('/wimbledon', methods=['GET'])
@require_auth
def get_wimbledon_final():
    try:
        # Get year from query parameters
        year_param = request.args.get('year')
        if not year_param:
            return jsonify({
                "error": "Missing required parameter 'year'",
                "message": "Please provide a year parameter (e.g., ?year=2021)"
            }), 400
        # Validate year
        year = validate_year(year_param)
        if year is None:
            return jsonify({
                "error": "Invalid year parameter",
                "message": "Year must be a valid integer between 1877 and 2024"
            }), 400
        # Load data for the specific year
        final_data = load_year_data(year)
        if final_data is None:
            return jsonify({
                "error": "Data not found",
                "message": f"No Wimbledon final data available for year {year}. Please check if the data extraction was successful."
            }), 404
        # Prepare response
        response_data = {
            "year": year,
            "champion": final_data["champion"],
            "runner_up": final_data["runner_up"],
            "score": format_score(final_data["score"]),
            "sets": final_data["sets"],
            "tiebreak": final_data["tiebreak"]
        }
        logger.info(f"Successfully retrieved data for year {year}")
        return jsonify(response_data), 200
    except Exception as e:
        logger.error(f"Unexpected error in get_wimbledon_final: {e}")
        return jsonify({
            "error": "Internal server error",
            "message": "An unexpected error occurred while processing your request"
        }), 500
@app.route('/wimbledon/player/<player_name>', methods=['GET'])
@require_auth
def get_player_finals(player_name):
    try:
        if not ensure_csv_exists():
            return jsonify({"error": "Data not available",}), 500
        player_name_lower = player_name.lower()
        finals = []
        with open('wimbledon_finals.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                champion = row['champion'].strip().lower()
                runner_up = row['runner_up'].strip().lower()
                if player_name_lower in (champion, runner_up):
                    finals.append({
                        "year": int(row['year']),
                        "champion": row['champion'].strip(),
                        "runner_up": row['runner_up'].strip(),
                        "score": format_score(row['score']),
                        "sets": int(row['sets']),
                        "tiebreak": bool(int(row.get('tiebreak', '0'))),
                        "player_won":player_name_lower == champion
                    })
        if not finals:
            return jsonify({
                "error": "No finals found",
                "message": f"No Wimbledon finals found for player '{player_name}'"
            }), 404
        finals.sort(key=lambda x: x['year'], reverse=True)
        return jsonify({
            "player_search": player_name,
            "total_finals": len(finals),
            "wins": sum(1 for f in finals if f['player_won']),
            "losses": sum(1 for f in finals if not f['player_won']),
        }), 200
    except Exception as e:
        logger.error(f"Unexpected error in get_player_finals: {e}")
        return jsonify({
            "error": "Internal server error",
            "message": "An unexpected error occurred while processing your request"
        }), 500
    
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)