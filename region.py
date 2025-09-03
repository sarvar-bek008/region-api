from fastapi import FastAPI, Request
import requests

app = FastAPI()

def get_player_info(Id):    
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
        "login_id": f"{Id}",
        "app_server_id": 0,
    }
    response = requests.post(url, headers=headers, json=payload)
    return response

@app.get("/region")
async def region(uid: str = None):
    if not uid:
        return {"message": "Please provide a UID"}
    
    response = get_player_info(uid)
    
    try:
        if response.status_code == 200:
            original_response = response.json()
            if not original_response.get('nickname') and not original_response.get('region'):
                return {"message": "UID not found, please check the UID"}
            
            return {
                "uid": uid,
                "nickname": original_response.get('nickname', ''),
                "region": original_response.get('region', '')
            }
        else:
            return {"message": "UID not found, please check the UID"}
    except Exception:
        return {"message": "UID not found, please check the UID"}
