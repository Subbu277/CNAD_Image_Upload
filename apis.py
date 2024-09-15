import time
from datetime import datetime

from flask import request, jsonify, Blueprint, send_from_directory

from bucket import upload_image, bucket
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
    public_url = upload_image(bucket ,image, bucket_object_name)
    return jsonify({"message": "Image uploaded successfully", "url": public_url}), 200


@health_api.route('/health', methods=['GET'])
def health():
    time.sleep(5)
    return jsonify({"message": "Server Health : Running"}), 200

@ui_api.route('/')
def index():
    return send_from_directory('templates', 'upload.html')
