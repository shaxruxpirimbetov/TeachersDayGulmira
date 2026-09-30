from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
data = []

@app.route("/")
def index_view():
	return render_template("index.html")

@app.route("/data", methods=["GET", "POST"])
def data_route():
	if request.method == "POST":
		text = request.json.get("text")
		data.append(text)
		return jsonify({"ok": True}), 201
	return jsonify(data), 200

if __name__ == "__main__":
	app.run()