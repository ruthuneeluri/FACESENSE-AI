import os
import cv2
import numpy as np
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
from database import db, AnalysisHistory

# Import local predictors
from face_detector import FaceAnalyzer
from age_predictor import AgePredictor
from emotion_predictor import EmotionPredictor
from smile_predictor import SmilePredictor

app = Flask(__name__)
CORS(app)

# Setup Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///history.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
db.init_app(app)

face_analyzer = FaceAnalyzer()
age_predictor = AgePredictor()
emotion_predictor = EmotionPredictor()
smile_predictor = SmilePredictor()

with app.app_context():
    db.create_all()

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})

@app.route('/api/analyze', methods=['POST'])
def analyze():
    if 'image' not in request.files:
        return jsonify({"success": False, "error": "No image provided"}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({"success": False, "error": "No selected file"}), 400
        
    filename = secure_filename(file.filename)
    if not filename:
        filename = "capture.jpg"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    img = cv2.imread(filepath)
    if img is None:
        return jsonify({"success": False, "error": "Invalid image format"}), 400
        
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
        
        history_entry = AnalysisHistory(
            image_path=filename,
            faces_detected=len(results_faces),
            estimated_age=str(results_faces[0]['estimated_age']) if results_faces else None,
            smile_score=str(results_faces[0]['smile']['score']) if results_faces else None,
            dominant_emotion=results_faces[0]['emotion']['dominant'] if results_faces else None
        )
        db.session.add(history_entry)
        db.session.commit()

        return jsonify({
            "success": True,
            "faces_detected": len(results_faces),
            "image_url": f"http://localhost:5000/api/image/{filename}",
            "faces": results_faces
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"success": False, "error": "Analysis failed on backend"}), 500

@app.route('/api/image/<filename>', methods=['GET'])
def get_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/api/history', methods=['GET'])
def get_history():
    records = AnalysisHistory.query.order_by(AnalysisHistory.timestamp.desc()).all()
    results = []
    for r in records:
        results.append({
            "id": r.id,
            "image_url": f"http://localhost:5000/api/image/{r.image_path}",
            "timestamp": r.timestamp.isoformat(),
            "faces_detected": r.faces_detected,
            "estimated_age": r.estimated_age,
            "smile_score": r.smile_score,
            "dominant_emotion": r.dominant_emotion
        })
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000, threaded=False)
