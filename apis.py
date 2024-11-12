import base64
import time
from datetime import datetime
from flask import request, jsonify, Blueprint, send_from_directory
import os
from db import add_user_upload_record, fetch_user_uploads_by_email
from google_cloud import upload_file,upload_to_gemini
from helpers import allowed_file

upload_api = Blueprint('upload', __name__)
health_api = Blueprint('health', __name__)
ui_api = Blueprint('ui', __name__)

@upload_api.route('/upload', methods=['POST'])
def upload():
    try:
        if 'image' not in request.files:
            return jsonify({"error": "No file part in the request"}), 400

        image = request.files['image']

        if not allowed_file(image.filename):
            return jsonify({"error": "Uploaded file is not an allowed image type"}), 400

        user_email = request.form.get('email')
        if not user_email:
            return jsonify({"error": "No email provided"}), 400

        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        local_path = f"temp_{timestamp}_{image.filename}"
        image.save(local_path)
        image.seek(0)

        try:
            upload_file(image, f"{timestamp}/{local_path}")
        except Exception as e:
            os.remove(local_path)
            return jsonify({"error": f"Failed to upload image"}), 500

        try:
            text, txt_url = upload_to_gemini(local_path, timestamp)
        except Exception as e:
            os.remove(local_path)
            return jsonify({"error": f"Failed to upload transcript"}), 500

        data = {
            'email': user_email,
            'image_path': f"{timestamp}/{local_path}",
            'transcript': text,
            'text_path': f"{timestamp}/{txt_url}"
        }
        try:
            add_user_upload_record(data)
        except Exception as e:
            os.remove(local_path)
            return jsonify({"error": f"Failed to save record"}), 500

        with open(local_path, "rb") as img_file:
            encoded_image = base64.b64encode(img_file.read()).decode('utf-8')

        response = {
            'image': f"data:image/{image.mimetype.split('/')[1]};base64,{encoded_image}",
            'transcript': text,
        }

        # Clean up the temporary file
        os.remove(local_path)

        return jsonify({"result": response}), 200

    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500


@upload_api.route('/uploads', methods=['GET'])
def get_uploads_by_email():
    user_email = request.args.get('email')

    if not user_email:
        return jsonify({"error": "No email provided"}), 400

    records = fetch_user_uploads_by_email(user_email)

    if not records:
        return jsonify({"error": "No records found for this email"}), 404

    return jsonify({"uploads": records}), 200


@health_api.route('/health', methods=['GET'])
def health():
    time.sleep(5)
    return jsonify({"message": "Server Health : Running"}), 200

@ui_api.route('/')
def index():
    return send_from_directory('templates', 'upload.html')
