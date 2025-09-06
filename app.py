from flask import Flask, request, jsonify
import asyncio
from playwright.async_api import async_playwright
import requests

app = Flask(__name__)

async def get_tokens():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
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

def get_player_info(uid, session_key, datadome):
    url = "https://shop2game.com/api/auth/player_id_login"

    cookies = {
        "region": "MA",
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

    res = requests.post(url, cookies=cookies, headers=headers, json=json_data)
    return res.json()

@app.route("/region", methods=["GET"])
def region_info():
    uid = request.args.get("uid")
    if not uid:
        return jsonify({"error": "UID is required"}), 400

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    session_key, datadome = loop.run_until_complete(get_tokens())

    if not session_key or not datadome:
        return jsonify({"error": "Failed to get tokens"}), 500

    data = get_player_info(uid, session_key, datadome)
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
