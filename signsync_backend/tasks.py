import json
import numpy as np
from tensorflow.keras.models import load_model
from app import celery, db
from models import Translation

# Load the ML model and label map
sign_model = load_model('../ml_model/sign_language_model.h5')
with open('../ml_model/label_map.json', 'r') as f:
    label_map = json.load(f)
reverse_label_map = {v: k for k, v in label_map.items()}

@celery.task
def process_video_task(meeting_id, video_path):
    # Simulate video processing (since actual upload isn't implemented)
    # In production, video_path would be used with process_video.py's inference
    predicted_class = 0  # Placeholder: "hello" (class 0 in label_map)
    translation = reverse_label_map.get(predicted_class, "unknown")

    # Save translation to database
    translation_entry = Translation(meeting_id=meeting_id, text=translation)
    db.session.add(translation_entry)
    db.session.commit()

    return translation