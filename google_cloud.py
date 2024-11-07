from google.cloud import storage
import os
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

model = genai.GenerativeModel(model_name="gemini-1.5-flash")
PROMPT = 'describe the image in 100 words'

def upload_to_gemini(path, dir):
    img = genai.upload_file(path)
    parts = [img, PROMPT]
    response = model.generate_content(parts)
    image_name=path.split(".")[0]
    txt_file_name = image_name +".txt"
    with open(txt_file_name, 'w') as txt_file:
        txt_file.write(response.text)

    with open(txt_file_name, 'rb') as txt_file:
        txt_url=upload_file(txt_file, dir+"/"+txt_file_name)
    os.remove(txt_file_name)
    return response.text,txt_url

