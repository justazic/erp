from django.urls import path
import teachers.views as views
app_name = 'teachers'
urlpatterns = [
    path('admin/list/', views.AdminTeacherListView.as_view(), name='admin_list'),
    path('admin/create/', views.AdminTeacherCreateView.as_view(), name='admin_create'),
    path('admin/<int:pk>/edit/', views.AdminTeacherEditView.as_view(), name='admin_edit'),
    path('admin/<int:pk>/delete/', views.AdminTeacherDeleteView.as_view(), name='admin_delete'),
    path('<int:pk>/', views.TeacherListView.as_view(), name='detail'),
    path('my-groups/', views.MyGroupsListView.as_view(), name='my_groups'),
    path('group/<int:group_id>/students/', views.GroupStudentsListView.as_view(), name='group_students'),
]