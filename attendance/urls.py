from django.urls import path
from .views import AttendanceCreateView

urlpatterns = [
    path('create/', AttendanceCreateView.as_view(), name='attendance_create'),
]
