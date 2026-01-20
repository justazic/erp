from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.AttendanceCreateView.as_view(), name='attendance_create'),
]

