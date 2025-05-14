# signsync_backend/config.py
class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql://signsync_user:your_password@localhost/signsync_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'