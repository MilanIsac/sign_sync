import cv2
import numpy as np
import mediapipe as mp
import json
import os
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import LSTM, Dense, TimeDistributed
from tensorflow.keras.optimizers import Adam

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7)

def load_wlasl_data(data_dir, max_frames=30, max_videos=None):
    """Load and preprocess WLASL dataset from Kaggle."""
    json_path = os.path.join(data_dir, "wlasl2000.json")

    if not os.path.exists(json_path):
        raise FileNotFoundError(f"Annotation file not found: {json_path}")

    with open(json_path, 'r') as f:
        annotations = json.load(f)

    X, y = [], []
    label_map = {}
    label_idx = 0

    for entry in annotations:
        gloss = entry['gloss']
        if gloss not in label_map:
            label_map[gloss] = label_idx
            label_idx += 1

        # Kaggle dataset organizes videos in folders by gloss
        gloss_dir = os.path.join(data_dir, gloss)
        if not os.path.exists(gloss_dir):
            print(f"Gloss directory not found: {gloss_dir}")
            continue

        for instance in entry['instances']:
            video_id = instance['video_id']
            video_path = os.path.join(gloss_dir, f"{video_id}.mp4")
            if not os.path.exists(video_path):
                print(f"Video not found: {video_path}")
                continue

            # Extract landmarks
            landmarks = extract_landmarks(video_path, max_frames, instance.get('frame_start', 1), instance.get('frame_end', -1))
            X.append(landmarks)
            y.append(label_map[gloss])

            if max_videos and len(X) >= max_videos:
                break
        if max_videos and len(X) >= max_videos:
            break

    if not X:
        raise ValueError("No valid videos found for processing.")

    return np.array(X), np.array(y), label_map

def extract_landmarks(video_path, max_frames=30, frame_start=1, frame_end=-1):
    """Extract hand landmarks from a video, respecting frame boundaries."""
    cap = cv2.VideoCapture(video_path)
    landmarks_list = []
    frame_count = 0
    current_frame = 0

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if frame_end == -1:
        frame_end = total_frames

    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_start - 1)

    while cap.isOpened() and frame_count < max_frames and current_frame < frame_end:
        ret, frame = cap.read()
        if not ret:
            break
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)

        if results.multi_hand_landmarks:
            frame_landmarks = []
            for hand in results.multi_hand_landmarks[:2]:
                for lm in hand.landmark:
                    frame_landmarks.extend([lm.x, lm.y, lm.z])
            while len(frame_landmarks) < 126:
                frame_landmarks.append(0.0)
            landmarks_list.append(frame_landmarks)
        else:
            landmarks_list.append([0.0] * 126)

        frame_count += 1
        current_frame += 1

    cap.release()
    while len(landmarks_list) < max_frames:
        landmarks_list.append([0.0] * 126)
    landmarks_list = landmarks_list[:max_frames]
    return np.array(landmarks_list)

def create_model(input_shape=(30, 126), num_classes=3):
    """Create a CNN-LSTM model for sign language recognition."""
    model = Sequential([
        TimeDistributed(Dense(64, activation='relu'), input_shape=input_shape),
        LSTM(128, return_sequences=False),
        Dense(64, activation='relu'),
        Dense(num_classes, activation='softmax')
    ])
    model.compile(optimizer=Adam(learning_rate=0.001), loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    return model

def train_model(model, X_train, y_train, epochs=10, batch_size=32):
    """Train the model on the dataset."""
    model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, validation_split=0.2)
    model.save('sign_language_model.h5')

def inference(video_path, model_path='sign_language_model.h5'):
    """Run inference on a video and return the predicted class."""
    model = load_model(model_path)
    landmarks = extract_landmarks(video_path)
    landmarks = np.expand_dims(landmarks, axis=0)
    prediction = model.predict(landmarks)
    predicted_class = np.argmax(prediction, axis=1)[0]
    return predicted_class

def main():
    # Load dataset from Kaggle structure
    try:
        X_train, y_train, label_map = load_wlasl_data("../datasets/wlasl_kaggle", max_videos=100)
    except Exception as e:
        print(f"Error loading dataset: {e}")
        return

    # Train model
    num_classes = len(label_map)
    print(f"Training on {len(X_train)} videos with {num_classes} classes.")
    model = create_model(num_classes=num_classes)
    train_model(model, X_train, y_train)

    # Save label map for backend use
    with open("label_map.json", "w") as f:
        json.dump(label_map, f)

    # Test inference
    sample_video = "../datasets/wlasl_kaggle/hello/00428.mp4"
    if os.path.exists(sample_video):
        predicted_class = inference(sample_video)
        reverse_label_map = {v: k for k, v in label_map.items()}
        predicted_gloss = reverse_label_map.get(predicted_class, "unknown")
        print(f"Predicted sign: {predicted_gloss}")
    else:
        print("Sample video not found. Provide a video file for inference.")

if __name__ == "__main__":
    main()