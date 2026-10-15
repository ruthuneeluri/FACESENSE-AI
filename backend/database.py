from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class AnalysisHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_path = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    faces_detected = db.Column(db.Integer, default=0)
    estimated_age = db.Column(db.String(50), nullable=True) # E.g., "23, 40"
    smile_score = db.Column(db.String(50), nullable=True)
    dominant_emotion = db.Column(db.String(100), nullable=True)
