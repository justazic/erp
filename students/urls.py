from django.urls import path
from .views import StudentListView,StudentCreateView,StudentProfileView,StudentUpdateView,StudentToggleActiveView

urlpatterns = [
    path('', StudentListView.as_view(), name='list'),
    path('create/', StudentCreateView.as_view(), name='create'),
    path('profile/', StudentProfileView.as_view(), name='profile'),
    path('update/', StudentUpdateView.as_view(), name='update'),
    path('toggle/<int:student_id>/', StudentToggleActiveView.as_view(), name='toggle'),
]