import os
from pathlib import Path
import tensorflow as tf

class TembakauModel:
    def __init__(self):

        self.base_path = Path(__file__).resolve().parent
        self.model_path = self.base_path / "model_tembakau.keras"
        self.model = self.load_model()


    def load_model(self):
        try:
            model = tf.keras.models.load_model(
                self.model_path,
                compile=False
            )
            return model
        except Exception as e :
            return None

MODEL = TembakauModel()
class_names = [
    "Alternaria Leaf Spot",
    "Cercospora Leaf Spot",
    "Healthy Leaf"
]
