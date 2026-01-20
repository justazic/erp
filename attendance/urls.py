from django.urls import path

from .views import AttendanceCreateView, AttendanceListView

urlpatterns = [
    path('create/', AttendanceCreateView.as_view(), name='attendance_create'),
    path('list/', AttendanceListView.as_view(), name='attendance_list'),
]

