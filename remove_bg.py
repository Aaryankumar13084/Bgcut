from flask import Flask, request, send_file, jsonify
import os
import rembg
from PIL import Image
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/remove-bg": {"origins": "*"}})  # ✅ CORS को सही तरीके से Enable किया गया है

UPLOAD_FOLDER = "uploads"
PROCESSED_FOLDER = "processed"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return "🚀 Background Remove API is Running!"

@app.route("/remove-bg", methods=["POST"])
def remove_bg():
    if "image" not in request.files:
        return jsonify({"error": "No file uploaded!"}), 400

    file = request.files["image"]
    input_path = os.path.join(UPLOAD_FOLDER, file.filename)
    output_path = os.path.join(PROCESSED_FOLDER, file.filename)

    file.save(input_path)

    image = Image.open(input_path)
    result = rembg.remove(image)
    result.save(output_path, format="PNG")

    response = send_file(output_path, mimetype="image/png")
    response.headers["Access-Control-Allow-Origin"] = "*"  # ✅ अब CORS Error नहीं आएगा
    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)