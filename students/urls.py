from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
    path('list/', views.StudentListView.as_view(), name='student_list'),
    path('my-attendance/', views.MyAttendanceView.as_view(), name='my_attendance'),
]
