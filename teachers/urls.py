from django.urls import path
from .views import TeacherListView,TeacherCreateView,TeacherProfileView,TeacherUpdateView,TeacherDeleteView, TeacherGroupListView,TeacherGroupDetailView

app_name = 'teachers'

urlpatterns = [
    path('', TeacherListView.as_view(), name='list'),
    path('create/', TeacherCreateView.as_view(), name='create'),
    path('profile/', TeacherProfileView.as_view(), name='profile'),
    path('update/', TeacherUpdateView.as_view(), name='update'),
    path('delete/<int:teacher_id>/', TeacherDeleteView.as_view(), name='delete'),
    path('groups/', TeacherGroupListView.as_view(), name='teacher_groups'),
    path('groups/<int:group_id>/', TeacherGroupDetailView.as_view(), name='teacher_group_detail'),
]
