# app/utils/image.py
import os, io, uuid
from PIL import Image

BASE_UPLOAD_DIR = "app/uploads"
PUBLIC_DIR = "predictions"

FS_DIR = os.path.join(BASE_UPLOAD_DIR, PUBLIC_DIR)
os.makedirs(FS_DIR, exist_ok=True)

def save_resized_image(contents: bytes) -> str:
    img = Image.open(io.BytesIO(contents)).convert("RGB")
    img = img.resize((224, 224))

    filename = f"{uuid.uuid4()}.jpg"
    fs_path = os.path.join(FS_DIR, filename)
    img.save(fs_path, "JPEG", quality=90)

    return f"{PUBLIC_DIR}/{filename}"
