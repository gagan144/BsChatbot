from django.urls import path

from core import views


urlpatterns = [
    path('chatroom/<str:chat_server_name>/', views.chatroom, name="core__chatroom"),
    path('chat-server/create/', views.chatserver_create, name="core__chatserver_create"),
    path('post-message/', views.post_message, name="core__post_message"),
]