from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from celery import Celery
from config import Config

# Initialize Flask app
app = Flask(__name__, instance_relative_config=True)
app.config.from_object(Config)
app.config.from_pyfile('config.py')  # Load instance/config.py for sensitive data

# Initialize extensions
db = SQLAlchemy(app)
api = Api(app)

# Initialize Celery
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

# Function to register API routes (avoids circular imports)
def register_api_routes():
    from api import MeetingResource, MeetingListResource, ProcessVideoResource
    api.add_resource(MeetingListResource, '/api/meetings')
    api.add_resource(MeetingResource, '/api/meetings/<int:meeting_id>')
    api.add_resource(ProcessVideoResource, '/api/meetings/<int:meeting_id>/process')

# Register routes after app initialization
with app.app_context():
    register_api_routes()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)