from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/region', methods=['GET'])
def region():
    uid = request.args.get('uid')
    if not uid:
        return jsonify({"message": "Please provide a UID"}), 400
    
    url = f"https://www.public.freefireinfo.site/api/info/sg/{uid}?key=astute_ff"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if "nickname" in data:
            return jsonify({
                "uid": uid,
                "nickname": data.get("nickname", ""),
                "region": data.get("region", "")
            })
        else:
            return jsonify({"message": "UID not found"}), 404
    else:
        return jsonify({"message": "UID not found"}), 404

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
