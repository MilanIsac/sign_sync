import React, { useState } from 'react';
import { createMeeting } from '../api';
import { useNavigate } from 'react-router-dom';

function MeetingForm() {
    const [title, setTitle] = useState("");
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const handleSubmit = async () => {
        if (!title) {
            setError("Please enter a meeting title.");
            return;
        }
        setError("");
        setLoading(true);
        try {
            const meeting = await createMeeting(title);
            navigate(`/meeting/${meeting.id}`);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="meeting-form-container">
            <h2 className="subtitle">Create a New Meeting</h2>
            {error && (
                <div className="error-message">
                    {error}
                </div>
            )}
            <div className="form-group">
                <input
                    type="text"
                    value={title}
                    onChange={(e) => setTitle(e.target.value)}
                    placeholder="Enter meeting title"
                    className="form-input"
                />
                <button
                    onClick={handleSubmit}
                    disabled={loading}
                    className="submit-btn"
                >
                    {loading ? "Creating..." : "Create"}
                </button>
            </div>
        </div>
    );
}

export default MeetingForm;