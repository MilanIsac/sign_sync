import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import VideoConference from '../components/VideoConference';
import TranslationOutput from '../components/TranslationOutput';
import { fetchMeetingDetails } from '../api';

function MeetingDetail() {
    const { id } = useParams();
    const [meeting, setMeeting] = useState(null);
    const [translation, setTranslation] = useState("");
    const [error, setError] = useState("");

    useEffect(() => {
        const loadMeeting = async () => {
            try {
                const data = await fetchMeetingDetails(id);
                setMeeting(data);
            } catch (err) {
                setError(err.message);
            }
        };
        loadMeeting();
    }, [id]);

    if (!meeting) {
        return (
            <div className="meeting-detail-container">
                {error ? (
                    <div className="error-message">
                        {error}
                    </div>
                ) : (
                    <p className="no-meetings">Loading...</p>
                )}
            </div>
        );
    }

    return (
        <div className="meeting-detail-container">
            <h1 className="title">{meeting.title}</h1>
            {error && (
                <div className="error-message">
                    {error}
                </div>
            )}
            <VideoConference meetingId={meeting.id} onTranslation={setTranslation} />
            <TranslationOutput translation={translation} />
        </div>
    );
}

export default MeetingDetail;