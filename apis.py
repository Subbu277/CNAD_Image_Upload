import time
from datetime import datetime

from flask import request, jsonify, Blueprint, send_from_directory
import os
from google_cloud import upload_file,upload_to_gemini
from helpers import allowed_file

upload_api = Blueprint('upload', __name__)
health_api = Blueprint('health', __name__)
ui_api = Blueprint('ui', __name__)

@upload_api.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    image = request.files['image']

    if not allowed_file(image.filename):
        return jsonify({"error": "Uploaded file is not an allowed image type"}), 400

    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    bucket_object_name = timestamp+'_'+image.filename
    local_path = os.path.join("tmp", bucket_object_name)
    print("-------------3 : image path",local_path)
    print("---------------4 : dir exist or not",os.path.exists("tmp_dir"))
    image.save(local_path)
    image.seek(0)
    public_url = upload_file(image, "image_files/"+bucket_object_name)
    text=upload_to_gemini(local_path,timestamp)
    os.remove(local_path)
    return jsonify({"message": "Image uploaded successfully ", "Transcription": text, "url": public_url}), 200


@health_api.route('/health', methods=['GET'])
def health():
    time.sleep(5)
    return jsonify({"message": "Server Health : Running"}), 200

@ui_api.route('/')
def index():
    return send_from_directory('templates', 'upload.html')
