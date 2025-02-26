from flask import Flask, request, send_file
import cv2
import numpy as np
import rembg
import os
from flask_cors import CORS
from PIL import Image

app = Flask(__name__)
CORS(app)  # CORS को Enable करो

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
        return {"error": "No file uploaded!"}, 400

    file = request.files["image"]
    input_path = os.path.join(UPLOAD_FOLDER, file.filename)
    output_path = os.path.join(PROCESSED_FOLDER, file.filename)

    file.save(input_path)

    # Open Image using PIL
    image = Image.open(input_path)

    # Remove background
    result = rembg.remove(image)

    # Save output
    result.save(output_path, format="PNG")

    return send_file(output_path, mimetype="image/png")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)