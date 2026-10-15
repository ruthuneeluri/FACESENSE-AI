import React, { useState } from 'react';
import { UploadCloud, Camera, Image as ImageIcon } from 'lucide-react';
import UploadZone from '../components/UploadZone';
import CameraView from '../components/CameraView';
import ResultDashboard from '../components/ResultDashboard';

export default function Analyze() {
    const [mode, setMode] = useState('upload'); // 'upload' or 'camera'
    const [image, setImage] = useState(null);
    const [isAnalyzing, setIsAnalyzing] = useState(false);
    const [result, setResult] = useState(null);

    const handleAnalyze = async (imgFile) => {
        setImage(imgFile);
        setIsAnalyzing(true);

        const formData = new FormData();
        formData.append('image', imgFile);

        try {
            const resp = await fetch(import.meta.env.VITE_API_URL + '/api/analyze', {
                method: 'POST',
                body: formData,
            });
            const data = await resp.json();
            setResult(data);
        } catch (err) {
            console.error(err);
            setResult({ success: false, error: 'Failed to connect to backend.' });
        }
        setIsAnalyzing(false);
    };

    if (result) {
        return <ResultDashboard result={result} image={image} onReset={() => { setResult(null); setImage(null); }} />;
    }

    if (isAnalyzing) {
        return (
            <div className="analysis-loading">
                <div className="loader"></div>
                <h2>Analyzing your face...</h2>
                <p>Detecting face, estimating age, and analyzing emotions...</p>
            </div>
        );
    }

    return (
        <div className="analyze-page">
            <h2>Analyze your face</h2>
            <p>Upload a clear front-facing photo or use your camera</p>

            <div className="mode-toggle">
                <button className={mode === 'upload' ? 'active' : ''} onClick={() => setMode('upload')}>Upload Photo</button>
                <button className={mode === 'camera' ? 'active' : ''} onClick={() => setMode('camera')}>Use Camera</button>
            </div>

            <div className="capture-area">
                {mode === 'upload' ? (
                    <UploadZone onPhotoSelected={handleAnalyze} />
                ) : (
                    <CameraView onPhotoCaptured={handleAnalyze} />
                )}
            </div>
        </div>
    );
}
