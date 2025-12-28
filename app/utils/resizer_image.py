# app/utils/image.py
import os, io, uuid
from PIL import Image

UPLOAD_DIR = "app/uploads/predictions"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def save_resized_image(contents: bytes) -> str:
    img = Image.open(io.BytesIO(contents)).convert("RGB")
    img = img.resize((224, 224))

    filename = f"{uuid.uuid4()}.jpg"
    file_path = os.path.join(UPLOAD_DIR, filename)
    img.save(file_path, "JPEG", quality=90)

    return file_path
