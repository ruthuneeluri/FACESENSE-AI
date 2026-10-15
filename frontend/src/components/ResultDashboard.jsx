import React, { useState } from 'react';

export default function ResultDashboard({ result, image, onReset }) {
    const [selectedFace, setSelectedFace] = useState(0);

    if (!result || !result.success) {
        return (
            <div className="result-error">
                <h3>Oops, something went wrong</h3>
                <p>{result?.error || 'Unknown error occurred.'}</p>
                <button className="btn btn-primary" onClick={onReset}>Try Again</button>
            </div>
        );
    }

    if (result.faces_detected === 0) {
        return (
            <div className="no-face">
                <h3>No face detected</h3>
                <p>We couldn't detect a clear face in this image. Try uploading a front-facing photo with good lighting.</p>
                <button className="btn btn-primary" onClick={onReset}>Try Another Photo</button>
            </div>
        );
    }

    const activeFace = result.faces[selectedFace];
    const imageUrl = image instanceof Blob ? URL.createObjectURL(image) : result.image_url;

    return (
        <div className="result-dashboard">
            <header className="dashboard-header">
                <h2>Your Face Analysis</h2>
                <button className="btn btn-secondary" onClick={onReset}>Analyze New Photo</button>
            </header>

            <div className="dashboard-layout">
                <div className="image-panel">
                    <div className="image-wrapper">
                        <img src={imageUrl || ""} className="analyzed-image" alt="Analyzed face" />
                        {/* Draw bounding boxes conceptually */}
                        {result.faces.map((f, i) => (
                            <div
                                key={f.face_id}
                                className={`bounding-box ${selectedFace === i ? 'active' : ''}`}
                                style={{
                                    left: f.bounding_box?.x ? `${f.bounding_box.x}%` : 'auto',
                                    top: f.bounding_box?.y ? `${f.bounding_box.y}%` : 'auto',
                                    width: f.bounding_box?.width ? `${f.bounding_box.width}%` : 'auto',
                                    height: f.bounding_box?.height ? `${f.bounding_box.height}%` : 'auto',
                                    border: selectedFace === i ? '3px solid #6366f1' : '3px solid #e5e7eb'
                                }}
                                onClick={() => setSelectedFace(i)}
                            >
                                <div className="box-label">Face {i + 1}</div>
                            </div>
                        ))}
                    </div>
                </div>

                <div className="summary-panel">
                    <div className="summary-cards">
                        <div className="card stat-card">
                            <h4>Faces Detected</h4>
                            <p>{result.faces_detected}</p>
                        </div>
                        <div className="card stat-card">
                            <h4>Estimated Age</h4>
                            <p>{activeFace.estimated_age}</p>
                        </div>
                        <div className="card stat-card">
                            <h4>Smile Score</h4>
                            <p>{Math.round(activeFace.smile.score)}%</p>
                        </div>
                        <div className="card stat-card">
                            <h4>Dominant Emotion</h4>
                            <p>{activeFace.emotion.dominant}</p>
                        </div>
                    </div>

                    <div className="card details-card">
                        <h3>SMILE ANALYSIS</h3>
                        <div className="smile-meter-container">
                            <div className="smile-meter">
                                <div className="smile-fill" style={{ width: `${activeFace.smile.score}%` }}></div>
                            </div>
                            <div className="smile-labels">
                                <span>Neutral</span>
                                <span style={{ color: 'var(--primary-color)', fontWeight: 'bold' }}>{Math.round(activeFace.smile.score)}% Intensity - {activeFace.smile.status}</span>
                                <span>Smiling</span>
                            </div>
                        </div>
                    </div>

                    <div className="card details-card">
                        <h3>EMOTION ANALYSIS</h3>
                        <div className="dominant-emotion-large">
                            <h4>{activeFace.emotion.dominant}</h4>
                            <span className="confidence-badge">{Math.round(activeFace.emotion.confidence)}% Confidence</span>
                        </div>
                        <div className="emotion-distribution">
                            {Object.entries(activeFace.emotion.distribution || {}).map(([emotion, score]) => (
                                <div className="dist-row" key={emotion}>
                                    <span className="dist-label">{emotion}</span>
                                    <div className="dist-bar-wrapper">
                                        <div className="dist-bar" style={{ width: `${score}%` }}></div>
                                    </div>
                                    <span className="dist-score">{Math.round(score)}%</span>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
