from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/region', methods=['GET'])
def region():
    uid = request.args.get('uid')
    if not uid:
        return jsonify({"message": "Please provide a UID"}), 400

    url = f"https://www.public.freefireinfo.site/api/info/sg/{uid}?key=astute_ff"

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        if "nickname" in data:
            return jsonify({
                "uid": uid,
                "nickname": data.get("nickname", ""),
                "region": data.get("region", "")
            })
        else:
            return jsonify({"message": "UID not found"}), 404
    except requests.exceptions.RequestException as e:
        return jsonify({"message": "API request failed", "error": str(e)}), 502
    except ValueError:
        return jsonify({"message": "Invalid response from API"}), 502

if __name__ == "__main__":
    app.run()
