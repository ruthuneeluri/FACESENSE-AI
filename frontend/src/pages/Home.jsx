import React from 'react';
import { Camera, Upload, ArrowRight } from 'lucide-react';
import { Link } from 'react-router-dom';

export default function Home() {
    return (
        <div className="home-page">
            <header className="hero">
                <h1>Understand Every Expression</h1>
                <p>AI-powered face analysis for estimated age, smile intensity and emotional expression.</p>
                <div className="hero-actions">
                    <Link to="/analyze" className="btn btn-primary">
                        <Upload className="icon" /> Analyze a Photo
                    </Link>
                    <Link to="/analyze?mode=camera" className="btn btn-secondary">
                        <Camera className="icon" /> Use Camera
                    </Link>
                </div>
            </header>
        </div>
    );
}
