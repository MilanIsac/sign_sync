# signsync_backend/api.py
from flask_restful import Resource, reqparse
from flask import request
from models import Meeting, Translation, User
from app import db
from tasks import process_video_feed

meeting_parser = reqparse.RequestParser()
meeting_parser.add_argument('title', type=str, required=True, help='Title is required')

class MeetingResource(Resource):
    def post(self):
        args = meeting_parser.parse_args()
        # For simplicity, use first user (implement authentication later)
        user = User.query.first() or User(username='test', password='test')
        if not User.query.first():
            db.session.add(user)
            db.session.commit()
        meeting = Meeting(title=args['title'], host_id=user.id)
        db.session.add(meeting)
        db.session.commit()
        return meeting.to_dict(), 201

class ProcessSignLanguageResource(Resource):
    def post(self, meeting_id):
        if 'video' not in request.files:
            return {'error': 'No video file provided'}, 400
        video_file = request.files['video']
        video_path = f'temp_{meeting_id}.mp4'
        video_file.save(video_path)
        # Use first user for simplicity
        user = User.query.first()
        if not user:
            return {'error': 'No user found'}, 400
        task = process_video_feed.delay(video_path, meeting_id, user.id)
        return {'task_id': task.id}, 202