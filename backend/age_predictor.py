import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input


class AgePredictor:
    def __init__(self):
        model_path = os.path.join(
            os.path.dirname(__file__),
            "models",
            "age_model_finetuned.keras"
        )

        self.model = tf.keras.models.load_model(model_path)

    def predict(self, face_rgb_image):
        try:
            # Resize image
            image = tf.image.resize(face_rgb_image, (160, 160))

            # Convert to float
            image = tf.cast(image, tf.float32)

            # MobileNetV2 preprocessing
            image = preprocess_input(image)

            # Add batch dimension
            image = tf.expand_dims(image, axis=0)

            # Predict age
            prediction = self.model.predict(image, verbose=0)

            age = float(prediction[0][0])

            # Keep age within reasonable range
            age = max(0, min(100, age))

            return round(age)

        except Exception as e:
            print("Age prediction error:", e)
            return "Error"