from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# 🔹 Configuration
VERIFY_TOKEN = "my_secure_token_123"  # Replace with your actual verify token
ACCESS_TOKEN = "EAAUHReb5GqEBO8CzBUBuaZARvY3zZAMTqbmKmrQXtDMuSJLohvM4FEJKqPCmcM2oH6KLysMiXHgUXMzX0SibwO3124qTymY4lHJIEdVayhOxDZAODMzpcs8tkfNFG43vC8CJZAPtGPSYFwlbZA29ZBhZAZA089nCTxk90oGHtx52HPg0sTFLeWUMMNoQOdZAjqkOj63nE1RZAuoAkTCj1eZB9fHgwG0"  # Replace with your actual access token
PHONE_NUMBER_ID = "581240415068867"  # Replace with your Meta Phone Number ID
WHATSAPP_NUMBER = "+15551505668"  # Your test WhatsApp number

# 🔹 Home Route (To Check If Bot is Running)
@app.route("/", methods=["GET"])
def home():
    return "WhatsApp Bot is Running!"

# 🔹 Webhook Route (For WhatsApp API)
@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        token_sent = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        if token_sent == VERIFY_TOKEN:
            return str(challenge)  # ✅ Ensure it returns a valid string
        return "Verification token mismatch", 403

    elif request.method == "POST":
        data = request.get_json()
        print("📩 Received Webhook Data:", data)  # Log incoming data

        try:
            if "entry" in data and "changes" in data["entry"][0] and "value" in data["entry"][0]["changes"][0]:
                if "messages" in data["entry"][0]["changes"][0]["value"]:
                    message = data["entry"][0]["changes"][0]["value"]["messages"][0]
                    sender_number = message["from"]
                    text = message["text"]["body"]

                    print(f"📞 Message from: {sender_number}")
                    print(f"💬 Text: {text}")

                    # ✅ Send Auto-Response
                    send_whatsapp_message(sender_number, f"✅ Hello! You wrote: {text}")
        except Exception as e:
            print(f"❌ Error processing message: {e}")

        return jsonify({"status": "received"}), 200

# 🔹 Function to Send WhatsApp Messages
def send_whatsapp_message(to_number, message_text):
    url = f"https://graph.facebook.com/v17.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to_number,
        "text": {"body": message_text}
    }

    response = requests.post(url, json=payload, headers=headers)
    print(f"📤 Message Sent: {response.status_code}, {response.text}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # ✅ Use Render's assigned port
    app.run(host="0.0.0.0", port=port)
