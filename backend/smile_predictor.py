
import cv2
import mediapipe as mp
import math


class SmilePredictor:

    def __init__(self):
        self.mp_face_mesh = mp.solutions.face_mesh

        self.face_mesh = self.mp_face_mesh.FaceMesh(
            static_image_mode=True,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5
        )

    def distance(self, p1, p2):
        return math.sqrt(
            (p1.x - p2.x) ** 2 +
            (p1.y - p2.y) ** 2
        )

    def predict(self, face_rgb_image):
        print("SMILE PREDICTOR CALLED")

        results = self.face_mesh.process(face_rgb_image)

        if not results.multi_face_landmarks:
            return {
                "score": 0.0,
                "status": "Neutral / Not Smiling"
            }

        landmarks = results.multi_face_landmarks[0].landmark

        # Mouth corners
        left_corner = landmarks[61]
        right_corner = landmarks[291]

        # Upper and lower lip
        upper_lip = landmarks[13]
        lower_lip = landmarks[14]

        # Face reference points
        left_eye = landmarks[33]
        right_eye = landmarks[263]

        # Calculate distances
        mouth_width = self.distance(left_corner, right_corner)
        mouth_opening = self.distance(upper_lip, lower_lip)
        eye_distance = self.distance(left_eye, right_eye)

        if eye_distance == 0:
            return {
                "score": 0.0,
                "status": "Neutral / Not Smiling"
            }

        # Normalize mouth measurements using eye distance
        width_ratio = mouth_width / eye_distance

        opening_ratio = (
            mouth_opening / mouth_width
            if mouth_width > 0 else 0
        )

        # Calculate smile score
        width_score = width_ratio * 80
        opening_score = opening_ratio * 20

        score = width_score + opening_score

        print(
            "DEBUG:",
            width_ratio,
            opening_ratio,
            width_score,
            opening_score,
            score
        )

        # Keep score between 0 and 100
        score = max(0.0, min(100.0, score))

        # Smile status
        if score < 20:
            status = "Neutral / Not Smiling"
        elif score < 40:
            status = "Slight Smile"
        elif score < 70:
            status = "Smiling"
        else:
            status = "Strong Smile"

        return {
            "score": round(score, 2),
            "status": status
        }

