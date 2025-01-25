import uuid


def generate_unique_file_name(extension) -> str:
    return f"{uuid.uuid4().hex}.{extension}"
