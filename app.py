import asyncio
import requests
from playwright.async_api import async_playwright


async def get_tokens(uid):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)  # headless=False qilsangiz browser oynasi ochiladi
        context = await browser.new_context()

        page = await context.new_page()
        await page.goto("https://shop2game.com/app/100067/idlogin")

        # Cookie va localStorage dan kerakli tokenlarni olish
        cookies = await context.cookies()
        local_storage = await page.evaluate("() => window.localStorage")

        session_key = None
        for c in cookies:
            if c.get("name") == "session_key":
                session_key = c.get("value")

        datadome_token = None
        for c in cookies:
            if c.get("name") == "datadome":
                datadome_token = c.get("value")

        await browser.close()

        return session_key, datadome_token


def get_player_info(uid, session_key, datadome_token):
    url = "https://shop2game.com/api/auth/player_id_login"

    cookies = {
        "region": "MA",
        "language": "ar",
        "session_key": session_key,
        "datadome": datadome_token,
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


async def main(uid):
    session_key, datadome_token = await get_tokens(uid)

    if not session_key or not datadome_token:
        print("❌ Tokenlarni olishda muammo chiqdi")
        return

    data = get_player_info(uid, session_key, datadome_token)
    print(data)


if __name__ == "__main__":
    # Misol uchun UID
    asyncio.run(main("1234567890"))
