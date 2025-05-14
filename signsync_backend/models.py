# signsync_backend/models.py
from flask_sqlalchemy import SQLAlchemy
from app import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def to_dict(self):
        return {'id': self.id, 'username': self.username}

class Meeting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    host_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    host = db.relationship('User', backref=db.backref('meetings', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'host_id': self.host_id,
            'created_at': self.created_at.isoformat(),
            'is_active': self.is_active
        }

class Translation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    meeting_id = db.Column(db.Integer, db.ForeignKey('meeting.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    meeting = db.relationship('Meeting', backref=db.backref('translations', lazy=True))
    user = db.relationship('User', backref=db.backref('translations', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'meeting_id': self.meeting_id,
            'user_id': self.user_id,
            'text': self.text,
            'created_at': self.created_at.isoformat()
        }