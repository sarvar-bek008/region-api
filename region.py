from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

def get_player_info(player_id):    
    url = "https://shop.garena.sg/api/auth/player_id_login"
    
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
        "Origin": "https://shop2game.com",
        "Referer": "https://shop2game.com/app",
        "X-Requested-With": "XMLHttpRequest",
    }
    
    payload = {
        "app_id": 100067,
        "login_id": player_id,
        "app_server_id": 0,
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        return response
    except Exception as e:
        print(f"So'rov xatosi: {str(e)}")
        return None

@app.route('/region', methods=['GET'])
def region():
    uid = request.args.get('uid')
    if not uid:
        return jsonify({"xabar": "Iltimos, UID ni kiriting"}), 200
    
    # UID ni tekshirish (faqat raqamlardan iborat bo'lishi kerak)
    if not uid.isdigit():
        return jsonify({"xabar": "Noto'g'ri UID formati. UID faqat raqamlardan iborat bo'lishi kerak"}), 200
    
    response = get_player_info(uid)
    
    if response is None:
        return jsonify({"xabar": "Tarmoq xatosi yuz berdi. Iltimos, keyinroq urunib ko'ring"}), 200
        
    try:
        if response.status_code == 200:
            original_response = response.json()
            
            # API dan qaytgan javobni tekshirish
            if 'nickname' in original_response and 'region' in original_response:
                return jsonify({
                    "uid": uid,
                    "nickname": original_response.get('nickname', ''),
                    "region": original_response.get('region', '')
                })
            else:
                return jsonify({"xabar": "UID topilmadi yoki serverda xatolik. Iltimos, UID ni tekshiring"}), 200
        else:
            return jsonify({
                "xabar": "Tizim so'rovlarni qayta ishlay olmayapti. Iltimos, keyinroq urunib ko'ring yoki boshqa UID bilan sinab ko'ring.",
            }), 200
    except Exception as e:
        print(f"Xato: {str(e)}")
        return jsonify({
            "xabar": "Ma'lumotlarni qayta ishlashda xatolik yuz berdi. Iltimos, keyinroq urunib ko'ring.",
        }), 200

@app.route('/')
def home():
    return jsonify({"xabar": "Server ishlamoqda. /region?uid=12345678 endpointiga so'rov yuboring"})

# Vercel uchun
app = app
