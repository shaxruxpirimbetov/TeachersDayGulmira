import requests
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

BOT_TOKEN = "8495367046:AAHYftXNwyZJ9onr5uG8L0yyU4KRkzFM5WE"
CHAT_ID = 8287944126

app = Flask(__name__)
CORS(app)
data = []  # запасная копия писем, видна по GET /data и на странице /#results


def send_to_telegram(text):
	try:
		r = requests.post(
			f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
			json={"chat_id": CHAT_ID, "text": text},
			timeout=10,
		)
	except requests.RequestException as e:
		app.logger.error("Telegram request failed: %s", e)
		return False
	if not r.ok:
		app.logger.error("Telegram error %s: %s", r.status_code, r.text)
	return r.ok


@app.route("/")
def index_view():
	return render_template("index.html")


@app.route("/data", methods=["GET", "POST"])
def data_route():
	if request.method == "POST":
		payload = request.get_json(silent=True) or {}
		text = payload.get("text")
		data.append(text)
		if not isinstance(text, str) or not text.strip():
			return jsonify({"ok": False, "error": "empty text"}), 400

		text = text.strip()[:3500]  # лимит Telegram: 4096 символов на сообщение
		message = "Новое письмо от Гульмиры Кенесбаевны:\n\n" + text

		if not send_to_telegram(message):
			return jsonify({"ok": False, "error": "telegram failed"}), 502

		return jsonify({"ok": True}), 201
	return jsonify(data), 200


if __name__ == "__main__":
	app.run()
