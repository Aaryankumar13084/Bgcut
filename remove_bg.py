from flask import Flask, request, jsonify
import rembg
from PIL import Image
import io
import base64
from flask_cors import CORS

app = Flask(__name__)

# CORS ko enable karein (sabhi origins ko allow karein)
CORS(app)

@app.route("/")
def home():
    return "🚀 Background Remove API is Running!"

@app.route("/remove-bg", methods=["POST", "OPTIONS"])
def remove_bg():
    # Preflight request ko handle karein (OPTIONS method)
    if request.method == "OPTIONS":
        response = jsonify({"message": "Preflight request received"})
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        response.headers.add("Access-Control-Allow-Methods", "POST")
        return response

    # Check karein ki image file upload ki gayi hai ya nahi
    if "image" not in request.files:
        return jsonify({"error": "No file uploaded!"}), 400

    # Image file ko receive karein
    file = request.files["image"]
    
    # Image ko PIL ke saath open karein
    image = Image.open(file.stream)

    # rembg library ka istemal karke background remove karein
    result = rembg.remove(image)

    # Processed image ko base64 format mein convert karein
    img_io = io.BytesIO()
    result.save(img_io, format="PNG")
    img_io.seek(0)
    img_base64 = base64.b64encode(img_io.read()).decode("utf-8")

    # Response mein base64 image return karein
    response = jsonify({"image": img_base64})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

# Server ko run karein
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)