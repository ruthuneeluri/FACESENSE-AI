import React from 'react';

export default function About() {
    return (
        <div style={{ maxWidth: '800px', margin: '3rem auto', padding: '0 1rem', lineHeight: '1.6' }}>
            <h1>How FaceSense AI Works</h1>

            <p style={{ fontSize: '1.1rem', color: '#475569', marginBottom: '2rem' }}>
                FaceSense AI uses advanced computer vision and machine learning models to analyze facial attributes in photos.
            </p>

            <div style={{ background: 'white', padding: '2rem', borderRadius: '1rem', boxShadow: '0 1px 3px rgba(0,0,0,0.1)' }}>
                <h3 style={{ marginTop: 0 }}>The Pipeline</h3>
                <ol style={{ paddingLeft: '1.5rem', display: 'flex', flexDirection: 'column', gap: '1rem', color: '#0f172a' }}>
                    <li><strong>Upload or capture a photo:</strong> Provide a clear, well-lit portrait.</li>
                    <li><strong>Face Detection:</strong> We use MediaPipe to identify one or more faces in the image.</li>
                    <li><strong>Facial Features:</strong> Blendshapes are extracted to evaluate smile intensity.</li>
                    <li><strong>Deep Learning Models:</strong> Cropped faces are passed to DeepFace to estimate age and predict dominant emotions (Happy, Sad, Angry, etc).</li>
                    <li><strong>Results:</strong> A detailed assessment is mapped out on our intuitive dashboard.</li>
                </ol>

                <h3 style={{ marginTop: '2rem' }}>Important Disclaimers</h3>
                <ul style={{ paddingLeft: '1.5rem', color: '#475569' }}>
                    <li><strong>Age is an estimate:</strong> Algorithms approximate age based on visual cues, which can vary wildly due to genetics, lighting, and makeup.</li>
                    <li><strong>Emotion is probabilistic:</strong> The classifier maps expression to the closest statistical match, not internal feelings.</li>
                    <li><strong>Privacy first:</strong> Uploaded images are stored locally only for the duration of the analysis or while retained in your history dashboard.</li>
                </ul>
            </div>
        </div>
    );
}
