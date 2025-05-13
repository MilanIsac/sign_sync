from django.urls import path
from . import views

urlpatterns = [
    path('meetings/', views.create_meeting, name='create_meeting'),
    path('meetings/<int:meeting_id>/process/', views.process_sign_language, name='process_sign_language'),
]