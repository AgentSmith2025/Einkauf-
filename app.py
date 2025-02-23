from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# 🔹 Конфигурация
VERIFY_TOKEN = "my_secure_token_123"  # Подставь свое значение
ACCESS_TOKEN = "EAAUHReb5GqEBO784Q5iEZAuqp0pj7fZAEWqT7YTzmuJNs3BsOIB8aH087ijbNp8gr60ywYnlnLZCHYBvVw4S1Ke9FYlfuavfQxyxfWgPxAmjZBSaBOkjbsGEp4ZA6aV1eSMgbbXJOHJqeQq4d51pvTArNoEQTBAAl0uYGK5tTtfFBExJFXvc53M13N97UJsVXDDd0StF7okpf7BNnKmg9cYCV"  # Подставь свой реальный токен
PHONE_NUMBER_ID = "581240415068867"  # ID номера из Meta
WHATSAPP_NUMBER = "+15551505668"  # Твой тестовый номер в WhatsApp

# 🔹 Главная страница
@app.route("/", methods=["GET"])
def home():
    return "WhatsApp Bot is Running!"

# 🔹 Вебхук
@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        token_sent = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        if token_sent == VERIFY_TOKEN:
            return challenge
        return "Verification token mismatch", 403

    elif request.method == "POST":
        data = request.get_json()
        print("📩 Входящее сообщение:", data)  # Логируем входящие данные

        # Проверяем, есть ли сообщение
        if "messages" in data["entry"][0]["changes"][0]["value"]:
            message = data["entry"][0]["changes"][0]["value"]["messages"][0]
            sender_number = message["from"]
            text = message["text"]["body"]

            print(f"📞 Сообщение от: {sender_number}")
            print(f"💬 Текст: {text}")

            # Отправляем автоответ
            send_whatsapp_message(sender_number, f"✅ Привет! Ты написал: {text}")

        return jsonify({"status": "received"}), 200

# 🔹 Функция отправки сообщений
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
    print(f"📤 Отправка сообщения: {response.status_code}, {response.text}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
