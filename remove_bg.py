from flask import Flask, request, jsonify
import rembg
from PIL import Image
import io
import base64
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "🚀 Background Remove API is Running!"

@app.route("/remove-bg", methods=["POST"])
def remove_bg():
    if "image" not in request.files:
        return jsonify({"error": "No file uploaded!"}), 400

    file = request.files["image"]
    image = Image.open(file.stream)

    # Background Remove करो
    result = rembg.remove(image)

    # Image को Base64 में Convert करो
    img_io = io.BytesIO()
    result.save(img_io, format="PNG")
    img_io.seek(0)
    img_base64 = base64.b64encode(img_io.read()).decode("utf-8")

    return jsonify({"image": img_base64})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)