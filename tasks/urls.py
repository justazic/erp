from django.urls import path

app_name = 'tasks'

urlpatterns = [
  path('assignments/', path, name='assignment_list'),
  path('submissions/teacher/', path, name='submission_list_teacher'),
  path('submissions/student/', path, name='submission_list_student'),
]
