from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
import numpy as np
from io import BytesIO
from utils import detect_emotion
from spotify import get_songs
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["musicapp"]
users = db["users"]

# Route: Register
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if users.find_one({"email": email}):
        return jsonify({"message": "User already exists"}), 400

    users.insert_one({
        "name": name,
        "email": email,
        "password": password,
        "progress": []
    })
    return jsonify({"message": "User registered successfully"}), 200

# Route: Login
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = users.find_one({"email": email, "password": password})
    if user:
        return jsonify({
            "name": user["name"],
            "email": user["email"],
            "progress": user.get("progress", [])
        }), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401

# Route: Image upload + Emotion detection
@app.route("/upload", methods=["POST"])
def upload():
    file = request.files.get("image")
    email = request.form.get("email")  # Passed in formData

    if not file:
        return jsonify({"emotion": None, "songs": []})

    img = Image.open(BytesIO(file.read())).convert("RGB")
    img_np = np.array(img)

    emotion = detect_emotion(img_np)
    if emotion and emotion != "No Face Detected":
        # Save progress to DB
        if email:
            users.update_one(
                {"email": email},
                {"$push": {"progress": emotion}}
            )
        songs = get_songs(emotion)
        return jsonify({"emotion": emotion, "songs": songs})
    else:
        return jsonify({"emotion": None, "songs": []})

# Route: Emotion from dropdown + songs
@app.route("/emotion", methods=["POST"])
def emotion():
    data = request.get_json()
    emotion = data.get("emotion")
    email = data.get("email")

    if not emotion:
        return jsonify({"error": "No emotion provided"}), 400

    # Save progress if user logged in
    if email:
        users.update_one(
            {"email": email},
            {"$push": {"progress": emotion}}
        )

    songs = get_songs(emotion)
    return jsonify({"emotion": emotion, "songs": songs})

# ✅ NEW Route: Get user's progress
@app.route("/user-progress", methods=["POST"])
def user_progress():
    data = request.get_json()
    email = data.get("email")

    if not email:
        return jsonify({"error": "Email required"}), 400

    user = users.find_one({"email": email})
    if user:
        return jsonify({"progress": user.get("progress", [])}), 200
    else:
        return jsonify({"progress": []}), 404

if __name__ == "__main__":
    app.run(port=5000)
