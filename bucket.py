from google.cloud import storage

def bucket_connection(bucket_name):
    storage_client = storage.Client()
    return storage_client.bucket(bucket_name)

def upload_image(bucket, image_file, bucket_object_name):
    blob = bucket.blob(bucket_object_name)
    blob.upload_from_file(image_file)
    return blob.public_url

bucket_name = "cnad_image_uploads"

bucket = bucket_connection(bucket_name)
