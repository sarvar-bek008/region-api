from fastapi import FastAPI
import requests

app = FastAPI()

def get_player_info(Id, server_id):
    url = "https://shop2game.com/api/auth/player_id_login"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Origin": "https://shop2game.com",
        "Referer": "https://shop2game.com/app",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
    }
    payload = {
        "app_id": 100067,
        "login_id": str(Id),
        "app_server_id": server_id,
    }
    response = requests.post(url, headers=headers, json=payload)
    return response

@app.get("/region")
async def region(uid: str = None):
    if not uid:
        return {"message": "Please provide a UID"}

    # Sinab ko‘ramiz 1 dan 10 gacha serverlarni
    for server_id in range(1, 11):
        response = get_player_info(uid, server_id)
        try:
            if response.status_code == 200:
                data = response.json()
                if data.get("nickname"):
                    return {
                        "uid": uid,
                        "nickname": data.get("nickname"),
                        "region": data.get("region", f"server-{server_id}"),
                        "server_id": server_id
                    }
        except Exception:
            continue
    
    return {"message": "UID not found in any server"}
