from django.urls import path

from core import views


urlpatterns = [
    path('chatroom/<str:chat_server_name>/', views.chatroom, name="core__chatroom"),
]