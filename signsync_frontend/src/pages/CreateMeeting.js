import React from 'react';
import MeetingForm from '../components/MeetingForm';

function CreateMeeting() {
    return (
        <div className="create-meeting-container">
            <h1 className="title">Create a New Meeting</h1>
            <MeetingForm />
        </div>
    );
}

export default CreateMeeting;