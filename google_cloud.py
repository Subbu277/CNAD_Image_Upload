from google.cloud import storage
import os
import google.generativeai as genai

api_key="AIzaSyDKPVGjK_69HwhUnMNg7_MBauYeXd78kAo"
genai.configure(api_key=api_key)

def bucket_connection(bucket_name):
    storage_client = storage.Client()
    return storage_client.bucket(bucket_name)

bucket_name = "cnad_image_uploads"
bucket_connection = bucket_connection(bucket_name)

def upload_file(file, bucket_object_name):
    blob = bucket_connection.blob(bucket_object_name)
    blob.upload_from_file(file)
    return blob.public_url

model = genai.GenerativeModel(model_name="gemini-1.5-flash")
PROMPT = 'describe the image'

def upload_to_gemini(path, image_name):
    img = genai.upload_file(path)
    parts = [img, PROMPT]
    response = model.generate_content(parts)
    txt_file_name = image_name+".txt"
    with open(txt_file_name, 'w') as txt_file:
        txt_file.write(response.text)

    with open(txt_file_name, 'rb') as txt_file:
        upload_file(txt_file, "text_files/"+txt_file_name)

    os.remove(txt_file_name)

    return response.text

