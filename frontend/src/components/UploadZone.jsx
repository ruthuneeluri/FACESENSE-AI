import React, { useCallback } from 'react';
import { UploadCloud } from 'lucide-react';

export default function UploadZone({ onPhotoSelected }) {
    const onDragOver = (e) => {
        e.preventDefault();
    };

    const onDrop = (e) => {
        e.preventDefault();
        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            handleFile(e.dataTransfer.files[0]);
        }
    };

    const onChange = (e) => {
        if (e.target.files && e.target.files[0]) {
            handleFile(e.target.files[0]);
        }
    };

    const handleFile = (file) => {
        // Validate size (10MB) and type
        if (file.size > 10 * 1024 * 1024) {
            alert('File size exceeds 10MB limit');
            return;
        }
        if (!file.type.match('image.*')) {
            alert('Only images are supported');
            return;
        }
        onPhotoSelected(file);
    };

    return (
        <div
            className="upload-zone"
            onDragOver={onDragOver}
            onDrop={onDrop}
        >
            <UploadCloud className="upload-icon" size={48} />
            <h3>Drop your image here</h3>
            <p>or click to browse (JPG, PNG, WEBP)</p>
            <input
                type="file"
                accept="image/jpeg, image/png, image/webp"
                onChange={onChange}
                id="fileInput"
                style={{ display: 'none' }}
            />
            <label htmlFor="fileInput" className="btn btn-primary">Browse Files</label>
        </div>
    );
}
