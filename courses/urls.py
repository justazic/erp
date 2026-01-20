from django.urls import path
from .views import (CourseCreateView,CourseListView,GroupCreateView,GroupListView,CommentCreateView,)

urlpatterns = [
    path('', CourseListView.as_view(), name='course_list'),
    path('create/', CourseCreateView.as_view(), name='course_create'),
    path('groups/', GroupListView.as_view(), name='group_list'),
    path('groups/create/', GroupCreateView.as_view(), name='group_create'),
    path('comment/add/', CommentCreateView.as_view(), name='comment_add'),
]
