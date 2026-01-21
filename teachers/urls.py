from django.urls import path
import teachers.views as views
app_name = 'teachers'
urlpatterns = [
    path('<int:pk>/', views.TeacherListView.as_view(), name='detail'),
    path('my-groups/', views.MyGroupsListView.as_view(), name='my_groups'),
    path('group/<int:group_id>/students/', views.GroupStudentsListView.as_view(), name='group_students'),
]