from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.utils import timezone
import uuid

from core.models import *
from core.chatbot import IntentBasedChatBot


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
    bot = IntentBasedChatBot()

    data = {
        "chat_server": chat_server,
        "bot": bot
    }
    return render(request, 'chat/chatroom.html', data)


@login_required
@require_http_methods(["POST"])
def post_message(request):
    """
    View to handle message being posted from chat.
    This view also sends back reply from the chat bot.
    """

    server_id = int(request.POST['server_id'])
    message = request.POST['message']

    user = request.user
    chat_server = ChatServer.objects.get(id=server_id)

    # Process message
    bot = IntentBasedChatBot()
    message_reply = bot.process(
        message = message,
        chatserver = chat_server,
        user = user
    )

    message_reply.update({
        "id": str(uuid.uuid4()),
        "user": {
            "username": bot.USERNAME,
            "name": bot.NAME
        },
        "datetime": timezone.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    })

    return JsonResponse({
        "status": "success",
        "reply": message_reply
    })




