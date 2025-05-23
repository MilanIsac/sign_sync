from flask_restful import Resource, reqparse
from app import db
from models import Meeting, Translation  # Import models here
from tasks import process_video_task

class MeetingListResource(Resource):
    def get(self):
        meetings = Meeting.query.all()
        return [meeting.to_dict() for meeting in meetings], 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str, required=True, help='Title is required')
        args = parser.parse_args()

        meeting = Meeting(title=args['title'])
        db.session.add(meeting)
        db.session.commit()

        return meeting.to_dict(), 201

class MeetingResource(Resource):
    def get(self, meeting_id):
        meeting = Meeting.query.get_or_404(meeting_id)
        return meeting.to_dict(), 200

class ProcessVideoResource(Resource):
    def post(self, meeting_id):
        # Verify meeting exists
        meeting = Meeting.query.get_or_404(meeting_id)

        # In production, handle file upload here
        # For now, simulate with a placeholder video path
        video_path = "../datasets/wlasl_kaggle/hello/00428.mp4"

        # Trigger Celery task for video processing
        result = process_video_task.delay(meeting_id, video_path)

        # Wait for the task to complete (for simplicity; in production, use a callback)
        translation = result.get(timeout=60)

        return {'translation': translation}, 200