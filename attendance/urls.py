from django.urls import path
from .views import MarkAttendanceView, ScheduleListView, ScheduleDetailView, MarkStudentAttendanceView, StudentSubmissionDetailView

app_name = 'attendance'

urlpatterns = [
    path('schedules/', ScheduleListView.as_view(), name='schedule_list'),
    path('schedule/<int:schedule_id>/', ScheduleDetailView.as_view(), name='schedule_detail'),
    path('schedule/<int:schedule_id>/mark/<int:student_id>/', MarkStudentAttendanceView.as_view(), name='mark_student_attendance'),
    path('submission/<int:submission_id>/', StudentSubmissionDetailView.as_view(), name='submission_detail'),
    path('mark/<int:schedule_id>/', MarkAttendanceView.as_view(), name='mark_attendance'),
    path('list/', ScheduleListView.as_view(), name='attendance_list'),
    path('create/', ScheduleListView.as_view(), name='attendance_create'),
]
