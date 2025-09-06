from flask import Flask, request, jsonify
import asyncio
from playwright.async_api import async_playwright
import requests

app = Flask(__name__)

# Playwright bilan token olish
async def fetch_tokens():
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True, args=["--no-sandbox"])
            context = await browser.new_context()
            page = await context.new_page()

            await page.goto("https://shop2game.com/app/100067/idlogin")

            cookies = await context.cookies()
            session_key = None
            datadome = None

            for c in cookies:
                if c.get("name") == "session_key":
                    session_key = c.get("value")
                if c.get("name") == "datadome":
                    datadome = c.get("value")

            await browser.close()
            return session_key, datadome
    except Exception as e:
        print("Playwright error:", e)
        return None, None

# UID bo'yicha player ma'lumot olish
def get_player_info(uid, session_key, datadome):
    url = "https://shop2game.com/api/auth/player_id_login"

    cookies = {
        "region": "RU",
        "language": "ar",
        "session_key": session_key,
        "datadome": datadome,
    }

    headers = {
        "Accept-Language": "en-US,en;q=0.9",
        "Origin": "https://shop2game.com",
        "Referer": "https://shop2game.com/app/100067/idlogin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/108.0.0.0 Safari/537.36",
        "accept": "application/json",
        "content-type": "application/json",
    }

    json_data = {
        "app_id": 100067,
        "login_id": uid,
        "app_server_id": 0,
    }

    try:
        res = requests.post(url, cookies=cookies, headers=headers, json=json_data, timeout=20)
        return res.json()
    except requests.exceptions.RequestException as e:
        return {"error": "HTTP request failed", "details": str(e)}

# Flask endpoint
@app.route("/region", methods=["GET"])
def region_info():
    uid = request.args.get("uid")
    if not uid:
        return jsonify({"error": "UID parameter is required"}), 400

    try:
        # Async Playwright token olish
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        session_key, datadome = loop.run_until_complete(fetch_tokens())

        if not session_key or not datadome:
            return jsonify({"error": "Failed to get session tokens"}), 500

        # Player info olish
        data = get_player_info(uid, session_key, datadome)
        return jsonify(data)

    except Exception as e:
        print("Server error:", e)
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
