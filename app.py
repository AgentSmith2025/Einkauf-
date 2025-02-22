from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Твои реальные данные
VERIFY_TOKEN = "my_secure_token_123"  # Подставь сюда свое значение
ACCESS_TOKEN = "EAAUHReb5GqEBOxAgCkSIvt2gtMwJPITm0b1J4g3ZChm4B1otzFWYcnm1rPVz9dvWkVroXHkCQpleAzOeLcLvBllMhMpbW1RHC8ACVVM5pOqcOsyaqaSZAlfoMvNRR8fj4WKEYrDy3OWqHheZC18ArRAQHZCZAhr6ffop6unkuR3ZBYGfJyBrCMn4V84ZAKIZCaZC6THTACoNYapjodpcwTUD0v0ZCx"  # Подставь свой реальный токен

@app.route("/", methods=["GET"])
def home():
    return "WhatsApp Bot is Running!"

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        # Подтверждение Webhook в Meta
        token_sent = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        if token_sent == VERIFY_TOKEN:
            return challenge
        return "Verification token mismatch", 403

    elif request.method == "POST":
        data = request.get_json()
        print("Received webhook data:", data)  # Логируем входящие сообщения
        return jsonify({"status": "received"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

