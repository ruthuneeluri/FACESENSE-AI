# FaceSenseAI 🧠📸
### AI-Based Facial Image Analysis for Age, Smile & Emotion Prediction

FaceSenseAI is an AI-powered web application that analyzes facial images to estimate age, detect facial emotions, and evaluate smiling behavior. It combines machine learning, computer vision, and web development to provide an interactive facial analysis experience through image uploads and camera capture.

## ✨ Features

- 🎂 **Age Prediction** — Estimates age from a detected face using a trained deep learning model.
- 😊 **Smile Analysis** — Analyzes facial landmarks and mouth features to estimate smile intensity.
- 🧠 **Emotion Detection** — Identifies the dominant facial emotion and provides confidence scores and emotion distribution.
- 📷 **Image Upload** — Upload an image for facial analysis.
- 🎥 **Camera Capture** — Capture an image directly through the browser camera.
- 📊 **Results Dashboard** — View age estimates, emotion predictions, and smile analysis results.
- 🕘 **Analysis History** — Access previously saved analysis results.
- 🔌 **REST API** — A Flask backend connects the frontend with the image analysis modules.

## 🛠️ Tech Stack

| Component | Technologies |
|---|---|
| Frontend | React.js, Vite, CSS |
| Backend | Python, Flask, Flask-CORS |
| Age Prediction | TensorFlow, Keras, MobileNetV2 |
| Emotion Detection | DeepFace |
| Face Detection | OpenCV Haar Cascade |
| Smile Analysis | MediaPipe Face Mesh and facial landmarks |
| Database | SQLite, Flask-SQLAlchemy |
| API Communication | REST API, JSON, FormData |

## 🏗️ Project Architecture

```text
FaceSenseAI/
│
├── backend/
│   ├── app.py
│   ├── database.py
│   ├── age_predictor.py
│   ├── emotion_predictor.py
│   ├── face_detector.py
│   ├── smile_predictor.py
│   ├── models/
│   │   └── age_model_finetuned.keras
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
│
├── ml/
│   ├── training/
│   ├── evaluation/
│   └── README.md
│
└── .gitignore
```

## ⚙️ How It Works

1. **Image Input:** The user uploads a facial image or captures one using the camera.
2. **Face Detection:** OpenCV detects the face and extracts the facial region.
3. **Age Estimation:** The trained age prediction model processes the face image and estimates age.
4. **Emotion Analysis:** DeepFace analyzes facial expressions and returns the dominant emotion, confidence, and emotion distribution.
5. **Smile Analysis:** Facial landmarks and mouth measurements are used to estimate smile intensity.
6. **Result Display:** The Flask API returns the analysis results to the React frontend for display.
7. **History Storage:** Analysis records can be stored in the SQLite database for later viewing.

## 🚀 Installation and Setup

### Prerequisites

- Python 3.11
- Node.js and npm
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/ruthuneeluri/FACESENSE-AI.git
cd FACESENSE-AI
```

### 2. Set Up the Backend

Open a terminal in the project root and run:

```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Keep the backend terminal running.

> If you use Command Prompt instead of PowerShell, activate the environment with `venv\Scripts\activate.bat`.

### 3. Set Up the Frontend

Open a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Open the local URL displayed by Vite in your browser.

### 4. Configure the API URL

Configure the frontend environment variable in `frontend/.env` to point to the Flask backend.

Example for a backend running locally on port 5000:

```env
VITE_API_URL=http://127.0.0.1:5000
```

Make sure this matches the port used by your Flask application. Restart the Vite development server after changing environment variables.

---

## 🔗 Backend API

The Flask backend provides endpoints for communication with the frontend.

| Endpoint | Method | Purpose |
|---|---|---|
| `/api/health` | GET | Check backend availability |
| `/api/analyze` | POST | Analyze an uploaded facial image |
| `/api/image/<filename>` | GET | Retrieve a saved image |
| `/api/history` | GET | Retrieve analysis history |

The analysis endpoint accepts an image using multipart form data with the field name `image`.

---

## 🎯 Project Objectives

- Integrate machine learning and computer vision into a web application.
- Perform face detection and facial image preprocessing.
- Estimate age and analyze facial expressions from images.
- Build an interactive interface using React and a REST API using Flask.
- Store and display analysis history.

---

## 🔮 Future Enhancements

- Improve prediction accuracy with more diverse training datasets.
- Enhance smile estimation across different lighting conditions and facial poses.
- Add more robust face detection and image quality checks.
- Deploy the frontend and backend for public access.
- Improve model evaluation and document performance metrics.

## ⚠️ Limitations and Disclaimer

FaceSenseAI provides experimental estimates, not verified measurements. Age, emotion, and smile predictions can be affected by image quality, lighting, face angle, occlusion, and model limitations. Facial emotion predictions do not reliably establish a person's actual feelings or mental state.

This project is intended for educational and demonstration purposes, not for medical, legal, employment, or other high-stakes decisions.

## 👩‍💻 Author

**Ruthu Neeluri**

GitHub: [@ruthuneeluri](https://github.com/ruthuneeluri)

**Project:** [FaceSenseAI](https://github.com/ruthuneeluri/FACESENSE-AI)

⭐ If you find this project interesting, consider starring the repository!
