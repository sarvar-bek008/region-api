from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

def get_player_info(Id):    
    url = "https://shop2game.com/api/auth/player_id_login"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Origin": "https://shop2game.com",
        "Referer": "https://shop2game.com/app",
    }
    payload = {
        "app_id": 100067,
        "login_id": Id,
        "app_server_id": 0,
    }
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        return response
    except Exception as e:
        print(f"Request error: {str(e)}")
        return None

@app.route('/region', methods=['GET'])
def region():
    uid = request.args.get('uid')
    if not uid:
        return jsonify({"message": "Please provide a UID"}), 200
    
    response = get_player_info(uid)
    
    if response is None:
        return jsonify({"message": "Network error occurred"}), 200
        
    try:
        print(f"Status code: {response.status_code}")
        print(f"Response text: {response.text}")
        
        if response.status_code == 200:
            original_response = response.json()
            print(f"Parsed response: {original_response}")
            
            if 'nickname' not in original_response or 'region' not in original_response:
                return jsonify({"message": "UID not found, please check the UID"}), 200
            
            return jsonify({
                "uid": uid,
                "nickname": original_response.get('nickname', ''),
                "region": original_response.get('region', '')
            })
        else:
            return jsonify({
                "message": "API request failed", 
                "status_code": response.status_code,
                "response": response.text[:200] + "..." if len(response.text) > 200 else response.text
            }), 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({
            "message": "Error processing response",
            "error": str(e)
        }), 200

@app.route('/')
def home():
    return jsonify({"message": "Server is running"})

# For Vercel deployment
app = app
