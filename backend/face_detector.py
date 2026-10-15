import cv2
import numpy as np
import os
import urllib.request

class FaceAnalyzer:
    def __init__(self):
        cascade_path = 'haarcascade_frontalface_default.xml'
        if not os.path.exists(cascade_path):
            url = 'https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml'
            urllib.request.urlretrieve(url, cascade_path)
            
        self.face_cascade = cv2.CascadeClassifier(cascade_path)

    def detect_faces(self, image_np):
        gray = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)
        # detectMultiScale returns (x, y, w, h)
        detections = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        
        faces = []
        h_img, w_img, _ = image_np.shape
        for idx, (x, y, w, h) in enumerate(detections):
            # Expand bounding box slightly
            padding = 0.2
            x_min = max(0, int(x - w * padding))
            y_min = max(0, int(y - h * padding * 2))
            width = min(w_img - x_min, int(w * (1 + padding * 2)))
            height = min(h_img - y_min, int(h * (1 + padding * 4)))

            faces.append({
                "face_id": idx + 1,
                "bounding_box": {
                    "x": (x_min / w_img) * 100, # Percentage
                    "y": (y_min / h_img) * 100,
                    "width": (width / w_img) * 100,
                    "height": (height / h_img) * 100
                },
                "crop_coords": (x_min, y_min, width, height)
            })
        return faces
