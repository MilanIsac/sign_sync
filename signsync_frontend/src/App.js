import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import CreateMeeting from './pages/CreateMeeting';
import MeetingDetail from './pages/MeetingDetail';
import './styles/App.css';

function App() {
    return (
        <Router>
            <div className="app-container">
                <Routes>
                    <Route path="/" element={<Home />} />
                    <Route path="/create-meeting" element={<CreateMeeting />} />
                    <Route path="/meeting/:id" element={<MeetingDetail />} />
                </Routes>
            </div>
        </Router>
    );
}

export default App;