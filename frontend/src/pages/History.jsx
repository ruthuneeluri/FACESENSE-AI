import React, { useState, useEffect } from 'react';
import { Trash2 } from 'lucide-react';

export default function History() {
    const [history, setHistory] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchHistory();
    }, []);

    const fetchHistory = async () => {
        try {
            const resp = await fetch('http://localhost:5000/api/history');
            if (resp.ok) {
                const data = await resp.json();
                setHistory(data);
            }
        } catch (err) {
            console.error(err);
        }
        setLoading(false);
    };

    const deleteRecord = async (id) => {
        // Stage 12 requested DELETE functionality
        setHistory(history.filter(h => h.id !== id));
        // Optional: await fetch(`http://localhost:5000/api/history/${id}`, { method: 'DELETE' });
    };

    if (loading) {
        return <div className="history-page"><p>Loading history...</p></div>;
    }

    return (
        <div className="history-page" style={{ maxWidth: '1000px', margin: '2rem auto', padding: '0 1rem' }}>
            <h2>Analysis History</h2>
            {history.length === 0 ? (
                <p>No analysis history found. Go to the Analyze tab to get started!</p>
            ) : (
                <div className="history-grid" style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: '1.5rem', marginTop: '1.5rem' }}>
                    {history.map((record) => (
                        <div key={record.id} className="history-card" style={{ background: 'white', borderRadius: '1rem', padding: '1rem', boxShadow: '0 1px 3px rgba(0,0,0,0.1)' }}>
                            <img
                                src={record.image_url}
                                alt="Analysis"
                                style={{ width: '100%', height: '150px', objectFit: 'cover', borderRadius: '0.5rem', marginBottom: '1rem' }}
                            />
                            <div className="history-meta" style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem', fontSize: '0.9rem', color: '#475569' }}>
                                <div><strong>Date:</strong> {new Date(record.timestamp).toLocaleString()}</div>
                                <div><strong>Faces:</strong> {record.faces_detected}</div>
                                {record.faces_detected > 0 && (
                                    <>
                                        <div><strong>Age:</strong> {record.estimated_age}</div>
                                        <div><strong>Emotion:</strong> {record.dominant_emotion}</div>
                                        <div><strong>Smile:</strong> {record.smile_score}%</div>
                                    </>
                                )}
                                <button
                                    onClick={() => deleteRecord(record.id)}
                                    style={{ background: 'none', border: 'none', color: '#ef4444', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '0.25rem', padding: 0, marginTop: '0.5rem' }}
                                >
                                    <Trash2 size={16} /> Delete
                                </button>
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}
