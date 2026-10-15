import cv2
import traceback
from face_detector import FaceAnalyzer
from smile_predictor import SmilePredictor
from age_predictor import AgePredictor
from emotion_predictor import EmotionPredictor

try:
    face_analyzer = FaceAnalyzer()
    smile_predictor = SmilePredictor()
    age_predictor = AgePredictor()
    emotion_predictor = EmotionPredictor()

    img = cv2.imread(r"C:\Users\Ruthu\.gemini\antigravity\brain\d5667750-ca9f-4e6c-9b0e-e4084d5ca4cc\one_face_1789985107207.png")
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    faces = face_analyzer.detect_faces(img_rgb)
    print("Faces detected:", len(faces))
    
    for f in faces:
        x, y, w, h = f['crop_coords']
        face_crop = img_rgb[y:y+h, x:x+w]
        
        print("Smile:", smile_predictor.predict(face_crop))
        print("Age:", age_predictor.predict(face_crop))
        print("Emotion:", emotion_predictor.predict(face_crop))
        
except Exception as e:
    traceback.print_exc()
