# signsync_backend/app.py
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from celery import Celery
from config import Config

app = Flask(__name__, instance_relative_config=True)
app.config.from_object(Config)
app.config.from_pyfile('config.py', silent=True)

# Initialize extensions
db = SQLAlchemy(app)
api = Api(app)
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

# Import and register API resources
from api import MeetingResource, ProcessSignLanguageResource
api.add_resource(MeetingResource, '/api/meetings')
api.add_resource(ProcessSignLanguageResource, '/api/meetings/<int:meeting_id>/process')

# Create database tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)