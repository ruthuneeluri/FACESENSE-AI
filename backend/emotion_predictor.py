from deepface import DeepFace


class EmotionPredictor:

    def __init__(self):
        pass

    def predict(self, face_rgb_image):
        try:
            analysis = DeepFace.analyze(
                face_rgb_image,
                actions=["emotion"],
                enforce_detection=False
            )

            result = analysis[0] if isinstance(analysis, list) else analysis

            emotion_confs = result.get("emotion", {})
            dominant = result.get("dominant_emotion", "neutral")

            distribution = {
                key: round(float(value), 1)
                for key, value in emotion_confs.items()
            }

            return {
                "dominant": dominant.capitalize(),
                "confidence": round(float(emotion_confs.get(dominant, 0)), 1),
                "distribution": distribution
            }

        except Exception as e:
            print("Emotion prediction error:", e)

            return {
                "dominant": "Error",
                "confidence": 0,
                "distribution": {}
            }