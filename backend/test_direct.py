import os
import cv2
from werkzeug.datastructures import FileStorage
from database import db, AnalysisHistory
from app import app, face_analyzer, age_predictor, emotion_predictor, smile_predictor

def simulate_request(filepath):
    print("Testing:", filepath)
    img = cv2.imread(filepath)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    try:
        faces_info = face_analyzer.detect_faces(img_rgb)
        results_faces = []
        for face_info in faces_info:
            x, y, w, h = face_info['crop_coords']
            x, y = max(0, x), max(0, y)
            w, h = min(img_rgb.shape[1]-x, w), min(img_rgb.shape[0]-y, h)
            
            face_crop = img_rgb[y:y+h, x:x+w]
            
            if face_crop.size == 0:
                continue
                
            age = age_predictor.predict(face_crop)
            emotion = emotion_predictor.predict(face_crop)
            smile = smile_predictor.predict(face_crop)
            
            face_data = {
                "face_id": face_info["face_id"],
                "bounding_box": face_info["bounding_box"],
                "estimated_age": age,
                "smile": smile,
                "emotion": emotion
            }
            results_faces.append(face_data)
        
        with app.app_context():
            history_entry = AnalysisHistory(
                image_path=os.path.basename(filepath),
                faces_detected=len(results_faces),
                estimated_age=str(results_faces[0]['estimated_age']) if results_faces else None,
                smile_score=str(results_faces[0]['smile']['score']) if results_faces else None,
                dominant_emotion=results_faces[0]['emotion']['dominant'] if results_faces else None
            )
            db.session.add(history_entry)
            db.session.commit()
            print("DB updated.")
        
        print("Success:", results_faces)

    except Exception as e:
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    simulate_request(r"C:\Users\Ruthu\.gemini\antigravity\brain\d5667750-ca9f-4e6c-9b0e-e4084d5ca4cc\one_face_1789985107207.png")
