from celery import shared_task
import cv2
import numpy as np
import mediapipe as mp
from tensorflow.keras.models import load_model
from .models import Meeting, Translation

sign_model = load_model('ml_model/sign_language_model.h5')

@shared_task
def process_video_feed(video_path, meeting_id, user_id):
    mp_hands = mp.solutions.hands.Hands()
    cap = cv2.VideoCapture(video_path)
    text_output = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = mp_hands.process(frame_rgb)

        if results.multi_hand_landmarks:
            landmarks = np.array([[lm.x, lm.y, lm.z] for hand in results.multi_hand_landmarks for lm in hand.landmark])
            landmarks = landmarks.reshape(1, -1)
            prediction = sign_model.predict(landmarks)
            text = decode_prediction(prediction)  # Custom function
            text_output.append(text)

    cap.release()
    text = ' '.join(text_output)
    Translation.objects.create(meeting_id=meeting_id, user_id=user_id, text=text)
    return text

def decode_prediction(prediction):
    # Placeholder: Map prediction to text (e.g., vocabulary lookup)
    return "hello"  # Replace with actual mapping