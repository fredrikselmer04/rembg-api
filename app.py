from flask import Flask, request, jsonify, send_file
from rembg import remove
import requests
from io import BytesIO

app = Flask(__name__)

@app.route("/remove-bg", methods=["POST"])
def remove_bg():
    data = request.json
    image_url = data.get("image_url")

    if not image_url:
        return jsonify({"error": "Missing image_url"}), 400

    try:
        response = requests.get(image_url)
        input_image = response.content
        output_image = remove(input_image)
        return send_file(BytesIO(output_image), mimetype="image/png")
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/")
def index():
    return "Rembg API is running!"
