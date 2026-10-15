import React, { useRef, useState, useEffect } from 'react';
import { Camera } from 'lucide-react';

export default function CameraView({ onPhotoCaptured }) {
    const videoRef = useRef(null);
    const streamRef = useRef(null);
    const [error, setError] = useState(null);

    useEffect(() => {
        startCamera();

        return () => {
            stopCamera();
        };
    }, []);

    const startCamera = async () => {
        try {
            const mediaStream = await navigator.mediaDevices.getUserMedia({
                video: {
                    width: { ideal: 1280 },
                    height: { ideal: 720 },
                    facingMode: "user"
                },
                audio: false
            });

            streamRef.current = mediaStream;

            if (videoRef.current) {
                videoRef.current.srcObject = mediaStream;
            }
        } catch (err) {
            console.error(err);
            setError(
                'Camera access denied or unavailable. Please check camera permissions.'
            );
        }
    };

    const stopCamera = () => {
        if (streamRef.current) {
            streamRef.current.getTracks().forEach(track => track.stop());
            streamRef.current = null;
        }
    };

    const capturePhoto = () => {
    if (!videoRef.current) return;

    const video = videoRef.current;

    if (video.videoWidth === 0 || video.videoHeight === 0) {
        setError('Camera is still loading. Please wait a moment and try again.');
        return;
    }

    const canvas = document.createElement('canvas');

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    const ctx = canvas.getContext('2d');

    // Camera image
    ctx.drawImage(
        video,
        0,
        0,
        canvas.width,
        canvas.height
    );

    // Improve brightness slightly
    const imageData = ctx.getImageData(
        0,
        0,
        canvas.width,
        canvas.height
    );

    const data = imageData.data;

    for (let i = 0; i < data.length; i += 4) {
        data[i] = Math.min(255, data[i] * 1.08 + 5);
        data[i + 1] = Math.min(255, data[i + 1] * 1.08 + 5);
        data[i + 2] = Math.min(255, data[i + 2] * 1.08 + 5);
    }

    ctx.putImageData(imageData, 0, 0);

    // Send image to backend
    canvas.toBlob(
        (blob) => {
            if (blob) {
                onPhotoCaptured(blob);
            }
        },
        'image/jpeg',
        0.95
    );
};

    if (error) {
        return <div className="camera-error">{error}</div>;
    }

    return (
        <div className="camera-view">
            <video
                ref={videoRef}
                autoPlay
                playsInline
                muted
            />

            <div className="camera-actions">
                <button
                    className="btn btn-primary"
                    onClick={capturePhoto}
                >
                    <Camera /> Capture
                </button>
            </div>
        </div>
    );
}