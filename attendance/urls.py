from django.urls import path
from .views import MarkAttendanceView, ScheduleListView

app_name = 'attendance'

urlpatterns = [
    path('schedules/', ScheduleListView.as_view(), name='schedule_list'),
    path('mark/<int:schedule_id>/', MarkAttendanceView.as_view(), name='mark_attendance'),
    path('list/', ScheduleListView.as_view(), name='attendance_list'),
    path('create/', ScheduleListView.as_view(), name='attendance_create'),
]
