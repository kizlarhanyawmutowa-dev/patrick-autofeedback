import os
import base64
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

@app.route("/win", methods=["POST"])
def win():
    try:
        data = request.json
        image_b64 = data.get("image")
        
        if not image_b64 or len(image_b64) < 100:
            return jsonify({"ok": False, "error": "NO_IMAGE"}), 400

        if "," in image_b64:
            image_b64 = image_b64.split(",")[1]
        
        image_data = base64.b64decode(image_b64)
        
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
        files = {"photo": ("win.jpg", image_data, "image/jpeg")}
        
        caption = f"👑 PATRICK JANE VIP 👑\n"
        caption += f"👤 {data.get('name', 'Unknown')}\n"
        caption += f"🆔 {data.get('uid', '0')}\n"
        caption += f"⭐ {data.get('rank_name', 'N/A')}\n"
        caption += f"💀 {data.get('kills', 0)} Kill"
        
        payload = {"chat_id": CHAT_ID, "caption": caption, "parse_mode": "HTML"}
        
        r = requests.post(url, files=files, data=payload, timeout=30)
        tg_res = r.json()
        
        # EĞER RESİM HATA VERİRSE, DÜZ YAZI OLARAK GÖNDER (TEST İÇİN)
        if not tg_res.get("ok"):
            text_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
            text_payload = {"chat_id": CHAT_ID, "text": caption, "parse_mode": "HTML"}
            requests.post(text_url, data=text_payload)
            return jsonify({"ok": True, "note": "Fotoğraf reddedildi, yazı gönderildi"})

        return jsonify({"ok": True})

    except Exception as e:
        return jsonify({"ok": False, "error": "SERVER_ERROR", "detail": str(e)}), 500

@app.route("/")
def home():
    return "VIP Auto Feedback is Running!"