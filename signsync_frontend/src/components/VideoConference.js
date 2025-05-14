import React, { useState } from 'react';
import { processVideo } from '../api';

function VideoConference({ meetingId, onTranslation }) {
    const [videoFile, setVideoFile] = useState(null);
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);

    const handleUpload = async () => {
        if (!videoFile) {
            setError("Please select a video file.");
            return;
        }
        setError("");
        setLoading(true);
        try {
            const result = await processVideo(meetingId);
            onTranslation(result.translation || "No translation available.");
        } catch (err) {
            setError(err.message);
            onTranslation("");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="video-conference-container">
            <h3 className="subtitle">Upload Video</h3>
            {error && (
                <div className="error-message">
                    {error}
                </div>
            )}
            <div className="upload-group">
                <input
                    type="file"
                    accept="video/*"
                    onChange={(e) => setVideoFile(e.target.files[0])}
                    className="upload-input"
                />
                <button
                    onClick={handleUpload}
                    disabled={loading}
                    className="process-btn"
                >
                    {loading ? "Processing..." : "Upload & Process"}
                </button>
            </div>
        </div>
    );
}

export default VideoConference;