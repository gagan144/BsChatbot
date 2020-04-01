from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.contrib.auth.decorators import login_required

from core.models import *


@login_required
def home(request):
    """
    View to handle home screen.
    """

    data = {
        # This could be a tastypie resource. But as of now, we are passing it through django template
        'list_servers': ChatServer.objects.filter(user=request.user)
    }
    return render(request, 'home.html', data)


@login_required
def chatroom(request, chat_server_name):
    """
    View to handle chatroom.
    """

    chat_server = ChatServer.objects.get(name=chat_server_name)

    data = {
        "chat_server": chat_server
    }
    return render(request, 'chat/chatroom.html', data)