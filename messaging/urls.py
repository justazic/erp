from django.urls import path
from . import views

app_name = 'messaging'

urlpatterns = [
    path('', views.GroupChatListView.as_view(), name='group_list'),
    path('chat/<int:group_id>/', views.GroupChatDetailView.as_view(), name='chat_detail'),
]
