# FaceSense AI - Machine Learning Environment

This directory contains the pipeline for training and evaluating models used in the FaceSense AI backend.

### Project Context
FaceSense AI is designed as a college Machine Learning and Computer Vision project. This module demonstrates the evaluation and potential fine-tuning of the utilized CNN architectures.

### Pretrained Models Used
Due to hardware constraints and dataset sizes, we utilize established state-of-the-art models for production deployment:
1. **Face Detection**: MediaPipe BlazeFace (Google) - excellent real-time performance.
2. **Age Estimation**: VGG-Face / DeepFace ensemble.
3. **Emotion Recognition**: Facial Expression Recognition (FER) DeepFace CNN.
4. **Smile Analysis**: MediaPipe FaceLandmarks (Heuristics based on 468 3D facial landmarks).

### Datasets (Recommended for retraining)
- **Age**: IMDB-WIKI dataset (500k+ images)
- **Emotion**: FER2013 dataset (35k+ expressions)
- **Smile**: CelebA dataset (Binary attributes)

### Structure
- `/datasets/`: Data loading scripts (e.g., pandas generators).
- `/training/`: Model definition and training loops using Keras/TensorFlow.
- `/evaluation/`: Metrics generation scripts (Accuracy, MAE, Confusion Matrix).
