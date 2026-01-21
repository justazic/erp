from django.urls import path
from . import views

app_name = 'courses'
urlpatterns = [
  path('', views.CourseListView.as_view(), name='list'),
  path('detail/<int:pk>/', views.CourseDetailCreateView.as_view(), name='detail'),
  path('admin/dashboard/', views.AdminDashboardView.as_view(), name='admin_dashboard'),
  path('admin/course/create/', views.CourseCreateView.as_view(), name='course_create'),
  path('admin/course/update/<int:pk>/', views.CourseUpdateView.as_view(), name='course_update'),
  path('admin/course/delete/<int:pk>/', views.CourseDeleteView.as_view(), name='course_delete'),
  path('admin/category/create/', views.CategoryCreateView.as_view(), name='category_create'),
  path('admin/category/update/<int:pk>/', views.CategoryUpdateView.as_view(), name='category_update'),
  path('admin/category/delete/<int:pk>/', views.CategoryDeleteView.as_view(), name='category_delete'),
  path('admin/group/create/', views.GroupCreateView.as_view(), name='group_create'),
  path('admin/group/update/<int:pk>/', views.GroupUpdateView.as_view(), name='group_update'),
  path('admin/group/delete/<int:pk>/', views.GroupDeleteView.as_view(), name='group_delete'),
  path('admin/session/create/', views.SessionCreateView.as_view(), name='session_create'),
  path('admin/session/update/<int:pk>/', views.SessionUpdateView.as_view(), name='session_update'),
  path('admin/session/delete/<int:pk>/', views.SessionDeleteView.as_view(), name='session_delete'),
  path('admin/students/', views.AdminStudentListView.as_view(), name='admin_student_list'),
  path('admin/students/create/', views.AdminStudentCreateView.as_view(), name='admin_student_create'),
  path('admin/students/<int:pk>/', views.AdminStudentDetailView.as_view(), name='admin_student_detail'),
  path('admin/students/<int:pk>/deposit/', views.AdminStudentDepositView.as_view(), name='admin_student_deposit'),
  path('admin/group/<int:pk>/students/manage/', views.AdminGroupStudentsView.as_view(), name='admin_group_students'),
]
