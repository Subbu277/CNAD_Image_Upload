import base64

from google.cloud import storage
import os
from PIL import Image
import google.generativeai as genai

api_key = os.getenv('GENAPI_API_KEY')
genai.configure(api_key=api_key)

def bucket_connection(bucket_name):
    storage_client = storage.Client()
    return storage_client.bucket(bucket_name)

bucket_name = "cnad_image_and_text_uploads"
bucket_connection = bucket_connection(bucket_name)

def upload_file(file, bucket_object_name):
    blob = bucket_connection.blob(bucket_object_name)
    blob.upload_from_file(file)
    return blob.public_url

def download_file(bucket_object_name, destination_file_path):
    blob = bucket_connection.blob(bucket_object_name)
    blob.download_to_filename(destination_file_path)
    with open(destination_file_path, "rb") as img_file:
        encoded_image = base64.b64encode(img_file.read()).decode('utf-8')
    return f"data:image/{destination_file_path};base64,{encoded_image}",

model = genai.GenerativeModel(model_name="gemini-1.5-flash")
PROMPT = 'describe the image in 100 words'

def upload_to_gemini(path, dir):
    img = Image.open(path)
    parts = [PROMPT,img]
    response = model.generate_content(parts,stream=True)
    response.resolve()

    image_name = path.split(".")[0]
    txt_file_name = image_name + ".txt"

    with open(txt_file_name, 'w') as txt_file:
        txt_file.write(response.text)

    with open(txt_file_name, 'rb') as txt_file:
        upload_file(txt_file, dir + "/" + txt_file_name)

    os.remove(txt_file_name)

    return response.text, txt_file_name

