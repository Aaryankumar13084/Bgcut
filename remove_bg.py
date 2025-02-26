from flask import Flask, request, jsonify
import rembg
from PIL import Image
import io
import base64
from flask_cors import CORS
import os

app = Flask(__name__)

# Enable CORS for all origins
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route("/", methods=["GET", "POST"])
def home():
    return "🚀 Background Remove API is Running!"

@app.route("/remove-bg", methods=["POST", "OPTIONS"])
def remove_bg():
    if request.method == "OPTIONS":
        response = jsonify({"message": "Preflight request received"})
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        response.headers.add("Access-Control-Allow-Methods", "POST")
        return response

    if "image" not in request.files:
        return jsonify({"error": "No file uploaded!"}), 400

    file = request.files["image"]
    try:
        image = Image.open(file.stream)
        result = rembg.remove(image)

        img_io = io.BytesIO()
        result.save(img_io, format="PNG")
        img_io.seek(0)
        img_base64 = base64.b64encode(img_io.read()).decode("utf-8")

        response = jsonify({"image": img_base64})
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response
    except Exception as e:
        return jsonify({"error": f"Error processing image: {str(e)}"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)