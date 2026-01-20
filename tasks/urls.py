from django.urls import path
from .views import AssigmentListView,AssigmentCreateView,AssigmentDeleteView,SubmissionCheckView,SubmissionCreateView,SubmissionsListTeacherView,MySubmissionListView

urlpatterns = [
    path('assignments/', AssigmentListView.as_view()),
    path('assignments/create/', AssigmentCreateView.as_view()),
    path('assignment/<int:assignment_id>/submit/', SubmissionCreateView.as_view()),
    path('my-submissions/', MySubmissionListView.as_view()),
    path('assignment/<int:assignment_id>/submissions/', SubmissionsListTeacherView.as_view()),
    path('submission/<int:submission_id>/check/', SubmissionCheckView.as_view()),
    path('assignment/<int:assignment_id>/delete/', AssigmentDeleteView.as_view()),
]