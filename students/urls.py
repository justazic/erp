from django.urls import path
from . import views

urlpatterns = [
  path('create/', views.StudentCreateView.as_view(), name='student_create'),
  path('list/', views.StudentListView.as_view(), name='student_list'),
]
