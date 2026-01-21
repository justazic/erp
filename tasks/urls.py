from django.urls import path
from . import views

app_name = 'tasks'

urlpatterns = [
    path('assignments/', views.AssigmentListView.as_view(), name='assignment_list'),
    path('assignments/create/', views.AssigmentCreateView.as_view(), name='assignment_create'),
    path('assignments/create/<int:group_id>/', views.AssigmentCreateView.as_view(), name='assignment_create'),
    path('assignments/<int:assignment_id>/edit/', views.AssigmentUpdateView.as_view(), name='assignment_edit'),
    path('assignments/delete/<int:assignment_id>/', views.AssigmentDeleteView.as_view(), name='assignment_delete'),
    path('submission/create/<int:assignment_id>/', views.SubmissionCreateView.as_view(), name='submission_create'),
    path('my-submissions/', views.MySubmissionListView.as_view(), name='my_submission_list'),
    path('submissions/teacher/<int:assignment_id>/', views.SubmissionsListTeacherView.as_view(), name='submission_list_teacher'),
    path('submission/check/<int:submission_id>/', views.SubmissionCheckView.as_view(), name='submission_check'),
]
