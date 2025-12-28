import numpy as np 
import io

from app.ml.model import MODEL,class_names
from PIL import Image 

def predict_from_bytes(image_bytes: bytes):
    if MODEL.model is None:
        raise RuntimeError("Model not loaded")

    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    img = img.resize((224, 224))

    img_array = np.expand_dims(np.array(img) / 255.0, axis=0)

    prediction = MODEL.model.predict(img_array)

    class_idx = int(np.argmax(prediction, axis=1)[0])
    confidence = float(np.max(prediction))

    return {
        "label": class_names[class_idx],
        "confidence": round(confidence * 100, 2)
    }