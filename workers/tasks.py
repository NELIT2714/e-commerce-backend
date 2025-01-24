import base64
import os

from cloudinary.exceptions import Error

from project.cloudinary import cloudinary, cloudinary_url
from project.functions import generate_unique_file_name
from workers import celery


@celery.task
def save_files(file_extension, file_content):
    try:
        if not file_content.startswith("data:image/"):
            raise ValueError("Invalid Base64 string for image")

        header, encoded = file_content.split(",", 1)
        file_data = base64.b64decode(encoded)
    except Exception as e:
        raise ValueError("Invalid Base64 string") from e

    unique_file_name = generate_unique_file_name(file_extension)
    file_path = os.path.join(os.getcwd(), "tmp", unique_file_name)

    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, "wb") as photo_file:
        photo_file.write(file_data)

    try:
        upload_result = cloudinary.uploader.upload(file_path, public_id=unique_file_name.split(".")[0])
    except Error as e:
        print(e)
        raise ValueError("Error uploading to Cloudinary") from e
