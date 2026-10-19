
import os
import uuid
import cv2
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
from database import db, AnalysisHistory

from face_detector import FaceAnalyzer
from age_predictor import AgePredictor
from emotion_predictor import EmotionPredictor
from smile_predictor import SmilePredictor

app = Flask(__name__)

CORS(app, allow_headers=["Content-Type", "X-User-ID"])

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///history.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'uploads'
)

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
db.init_app(app)

# Initialize ML models
face_analyzer = FaceAnalyzer()
age_predictor = AgePredictor()
emotion_predictor = EmotionPredictor()
smile_predictor = SmilePredictor()


# Create tables and add user_id to an existing database if needed
with app.app_context():
    db.create_all()

    columns = db.session.execute(
        db.text("PRAGMA table_info(analysis_history)")
    ).fetchall()

    column_names = [column[1] for column in columns]

    if columns and 'user_id' not in column_names:
        db.session.execute(
            db.text(
                "ALTER TABLE analysis_history "
                "ADD COLUMN user_id VARCHAR(100) "
                "NOT NULL DEFAULT 'default'"
            )
        )
        db.session.commit()


def get_user_id():
    """Get the browser ID sent by the frontend."""
    user_id = request.headers.get('X-User-ID', '').strip()

    if not user_id or len(user_id) > 100:
        return None

    return user_id


@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})


@app.route('/api/analyze', methods=['POST'])
def analyze():
    user_id = get_user_id()

    if not user_id:
        return jsonify({
            "success": False,
            "error": "User ID missing"
        }), 400

    if 'image' not in request.files:
        return jsonify({
            "success": False,
            "error": "No image provided"
        }), 400

    file = request.files['image']

    if not file.filename:
        return jsonify({
            "success": False,
            "error": "No selected file"
        }), 400

    original_name = secure_filename(file.filename)
    extension = os.path.splitext(original_name)[1].lower()

    if extension not in {'.jpg', '.jpeg', '.png', '.webp', '.bmp'}:
        return jsonify({
            "success": False,
            "error": "Unsupported image format"
        }), 400

    # Unique filename prevents different uploads overwriting each other
    filename = f"{uuid.uuid4().hex}{extension}"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    try:
        file.save(filepath)

        img = cv2.imread(filepath)

        if img is None:
            os.remove(filepath)
            return jsonify({
                "success": False,
                "error": "Invalid image format"
            }), 400

        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        faces_info = face_analyzer.detect_faces(img_rgb)

        results_faces = []

        for face_info in faces_info:
            x, y, w, h = face_info['crop_coords']

            x = max(0, x)
            y = max(0, y)
            w = min(img_rgb.shape[1] - x, w)
            h = min(img_rgb.shape[0] - y, h)

            if w <= 0 or h <= 0:
                continue

            face_crop = img_rgb[y:y + h, x:x + w]

            if face_crop.size == 0:
                continue

            age = age_predictor.predict(face_crop)
            emotion = emotion_predictor.predict(face_crop)
            smile = smile_predictor.predict(face_crop)

            results_faces.append({
                "face_id": face_info["face_id"],
                "bounding_box": face_info["bounding_box"],
                "estimated_age": age,
                "smile": smile,
                "emotion": emotion
            })

        history_entry = AnalysisHistory(
            user_id=user_id,
            image_path=filename,
            faces_detected=len(results_faces),
            estimated_age=(
                str(results_faces[0]['estimated_age'])
                if results_faces else None
            ),
            smile_score=(
                str(results_faces[0]['smile']['score'])
                if results_faces else None
            ),
            dominant_emotion=(
                results_faces[0]['emotion']['dominant']
                if results_faces else None
            )
        )

        db.session.add(history_entry)
        db.session.commit()

        image_url = (
            f"{request.host_url.rstrip('/')}/api/image/{filename}"
            f"?user_id={user_id}"
        )

        return jsonify({
            "success": True,
            "faces_detected": len(results_faces),
            "image_url": image_url,
            "faces": results_faces
        })

    except Exception:
        db.session.rollback()

        import traceback
        traceback.print_exc()

        return jsonify({
            "success": False,
            "error": "Analysis failed on backend"
        }), 500


@app.route('/api/image/<filename>', methods=['GET'])
def get_image(filename):
    user_id = request.args.get('user_id', '').strip()

    if not user_id or len(user_id) > 100:
        return jsonify({"error": "User ID missing"}), 400

    # Only return images associated with this browser ID
    record = AnalysisHistory.query.filter_by(
        image_path=filename,
        user_id=user_id
    ).first()

    if record is None:
        return jsonify({"error": "Image not found"}), 404

    return send_from_directory(
        app.config['UPLOAD_FOLDER'],
        filename
    )


@app.route('/api/history', methods=['GET'])
def get_history():
    user_id = get_user_id()

    if not user_id:
        return jsonify({
            "success": False,
            "error": "User ID missing"
        }), 400

    records = AnalysisHistory.query.filter_by(
        user_id=user_id
    ).order_by(
        AnalysisHistory.timestamp.desc()
    ).all()

    results = []

    for record in records:
        results.append({
            "id": record.id,
            "image_url": (
                f"{request.host_url.rstrip('/')}/api/image/"
                f"{record.image_path}?user_id={user_id}"
            ),
            "timestamp": record.timestamp.isoformat(),
            "faces_detected": record.faces_detected,
            "estimated_age": record.estimated_age,
            "smile_score": record.smile_score,
            "dominant_emotion": record.dominant_emotion
        })

    return jsonify(results)


if __name__ == '__main__':
    app.run(
        debug=False,
        host='0.0.0.0',
        port=5000,
        threaded=False
    )
