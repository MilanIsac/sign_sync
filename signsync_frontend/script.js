const API_URL = "http://localhost:5000"; // Adjust if using .env

// DOM Elements
const errorMessage = document.getElementById('error-message');
const meetingTitleInput = document.getElementById('meeting-title');
const createMeetingBtn = document.getElementById('create-meeting-btn');
const noMeetingsText = document.getElementById('no-meetings');
const meetingList = document.getElementById('meeting-list');
const videoSection = document.getElementById('video-section');
const videoSectionTitle = document.getElementById('video-section-title');
const videoInput = document.getElementById('video-input');
const processBtn = document.getElementById('process-btn');
const translationContainer = document.getElementById('translation-container');
const translationText = document.getElementById('translation-text');

let currentMeetingId = null;

// Show error message
function showError(message) {
    errorMessage.textContent = message;
    errorMessage.style.display = 'block';
    setTimeout(() => {
        errorMessage.style.display = 'none';
    }, 5000);
}

// Fetch and display meetings
async function fetchMeetings() {
    try {
        const response = await fetch(`${API_URL}/api/meetings`);
        if (!response.ok) throw new Error("Failed to fetch meetings");
        const meetings = await response.json();

        meetingList.innerHTML = '';
        if (meetings.length === 0) {
            noMeetingsText.style.display = 'block';
        } else {
            noMeetingsText.style.display = 'none';
            meetings.forEach(meeting => {
                const li = document.createElement('li');
                li.className = 'meeting-item';
                const div = document.createElement('div');
                div.className = 'meeting-link';
                div.textContent = `${meeting.title} (ID: ${meeting.id})`;
                div.addEventListener('click', () => selectMeeting(meeting));
                li.appendChild(div);
                meetingList.appendChild(li);
            });
        }
    } catch (err) {
        showError(err.message);
    }
}

// Create a new meeting
async function createMeeting() {
    const title = meetingTitleInput.value.trim();
    if (!title) {
        showError("Please enter a meeting title.");
        return;
    }

    createMeetingBtn.disabled = true;
    createMeetingBtn.textContent = "Creating...";

    try {
        const response = await fetch(`${API_URL}/api/meetings`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ title }),
        });
        if (!response.ok) throw new Error("Failed to create meeting");
        const meeting = await response.json();

        meetingTitleInput.value = '';
        await fetchMeetings();
        selectMeeting(meeting);
    } catch (err) {
        showError(err.message);
    } finally {
        createMeetingBtn.disabled = false;
        createMeetingBtn.textContent = "Create";
    }
}

// Select a meeting and show video upload section
function selectMeeting(meeting) {
    currentMeetingId = meeting.id;
    videoSectionTitle.textContent = `Upload Video for ${meeting.title}`;
    videoSection.style.display = 'block';
    translationContainer.style.display = 'none';
    videoInput.value = ''; // Reset file input
}

// Process video
async function processVideo() {
    if (!currentMeetingId) {
        showError("Please select a meeting.");
        return;
    }

    if (!videoInput.files[0]) {
        showError("Please select a video file.");
        return;
    }

    processBtn.disabled = true;
    processBtn.textContent = "Processing...";

    try {
        const response = await fetch(`${API_URL}/api/meetings/${currentMeetingId}/process`, {
            method: "POST",
        });
        if (!response.ok) throw new Error("Failed to process video");
        const result = await response.json();

        translationText.textContent = result.translation || "No translation available.";
        translationContainer.style.display = 'block';
    } catch (err) {
        showError(err.message);
        translationContainer.style.display = 'none';
    } finally {
        processBtn.disabled = false;
        processBtn.textContent = "Upload & Process";
    }
}

// Event Listeners
createMeetingBtn.addEventListener('click', createMeeting);
processBtn.addEventListener('click', processVideo);

// Initial Load
fetchMeetings();