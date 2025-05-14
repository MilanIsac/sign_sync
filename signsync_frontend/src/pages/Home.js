import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { fetchMeetings } from '../api';

function Home() {
    const [meetings, setMeetings] = useState([]);
    const [error, setError] = useState("");

    useEffect(() => {
        const loadMeetings = async () => {
            try {
                const data = await fetchMeetings();
                setMeetings(data);
            } catch (err) {
                setError(err.message);
            }
        };
        loadMeetings();
    }, []);

    return (
        <div className="home-container">
            <h1 className="title">SignSync Video Conference</h1>
            {error && (
                <div className="error-message">
                    {error}
                </div>
            )}
            <div>
                <Link to="/create-meeting">
                    <button className="create-meeting-btn">
                        Create New Meeting
                    </button>
                </Link>
            </div>
            <h2 className="meetings-heading">Meetings</h2>
            {meetings.length === 0 ? (
                <p className="no-meetings">No meetings available. Create one to get started.</p>
            ) : (
                <ul className="meeting-list">
                    {meetings.map((meeting) => (
                        <li key={meeting.id} className="meeting-item">
                            <Link to={`/meeting/${meeting.id}`} className="meeting-link">
                                {meeting.title} (ID: {meeting.id})
                            </Link>
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
}

export default Home;