from flask import Flask, request, jsonify
import asyncio
from playwright.async_api import async_playwright
import requests

app = Flask(__name__)

# --- Playwright bilan token olish ---
async def fetch_tokens():
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True, args=["--no-sandbox"])
            context = await browser.new_context()
            page = await context.new_page()
            
            # Misol uchun shop2game login sahifasi
            await page.goto("https://shop2game.com/login")
            
            # Sahifadan token yoki cookie olish
            # Masalan, session_key yoki datadome cookie
            cookies = await context.cookies()
            session_key = next((c['value'] for c in cookies if c['name'] == 'session_key'), None)
            datadome = next((c['value'] for c in cookies if c['name'] == 'datadome'), None)
            
            await browser.close()
            
            if not session_key or not datadome:
                return None, None
            return session_key, datadome
    except Exception as e:
        print("Playwright xato:", e)
        return None, None

# --- UID bo'yicha player ma'lumot olish ---
def get_player_info(uid, session_key, datadome):
    url = "https://shop2game.com/api/auth/player_id_login"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Cookie": f"session_key={session_key}; datadome={datadome}"
    }
    data = {"uid": uid}
    try:
        resp = requests.post(url, json=data, headers=headers)
        return resp.json()
    except Exception as e:
        return {"error": str(e)}

# --- Flask endpoint ---
@app.route("/region", methods=["GET"])
def region_info():
    uid = request.args.get("uid")
    if not uid:
        return jsonify({"error": "UID parameter is required"}), 400
    
    # Playwright bilan token olish (async)
    session_key, datadome = asyncio.run(fetch_tokens())
    if not session_key or not datadome:
        return jsonify({"error": "Failed to get session tokens"}), 500
    
    # UID bo'yicha ma'lumot olish
    player_info = get_player_info(uid, session_key, datadome)
    return jsonify(player_info)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
