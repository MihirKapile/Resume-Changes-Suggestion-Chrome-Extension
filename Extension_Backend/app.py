import os
from flask import Flask, request, jsonify

from ingest import ingest
from suggestions import generate_suggestions
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "./uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    job_description = data.get("description", "")

    suggestions = generate_suggestions(job_description)

    return jsonify({"suggestions": suggestions})


@app.route("/hello", methods=["GET"])
def hello():
    return "Hello, World!"


@app.route("/upload", methods=["POST"])
def upload_file():
    if "resume" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["resume"]

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if file and file.filename.endswith(".pdf"):
        file_path = os.path.join("./uploads", file.filename)
        file.save(file_path)

        ingest(file_path)
        return jsonify({"message": "File uploaded successfully"}), 200

    return jsonify({"error": "Invalid file type"}), 400


if __name__ == "__main__":
    app.run(port=8000)
