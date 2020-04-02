from googlesearch import search

from core.models import *


class IntentBasedChatBot:
    """
    Intent/Rule based chat bot. In this, we define 'intent' or keywords that
    we expect to receive along with the action to perform.
    """

    USERNAME = "bs_chatbot_v1"
    NAME = "Arya"

    def __init__(self):
        self.INTENTS = {
            "hi": self.action_hey,
            "!google": self.action_googleSearch,
            "!recent": self.action_searchHistory,
        }

    # --- Actions ---
    # All action methods must accept parameters: (self, msg, chatserver, user)

    def action_hey(self, msg, chatserver, user):
        return {
            "type": "text",
            "data": "hey"
        }

    def action_googleSearch(self, msg, chatserver, user):
        search_text = " ".join(msg.split()[1:])

        # Search via google api
        data = []
        for result in search(query=search_text, num=10, stop=5):
            data.append({
                "url": result
            })

        # Save in database
        hist = SearchHistory.objects.create(
            user = user,
            chat_server = chatserver,
            search_text = search_text
        )

        return {
            "type": "google_search",
            "query": search_text,
            "data": data
        }

    def action_searchHistory(self, msg, chatserver, user):
        search_text = " ".join(msg.split()[1:])

        list_history = SearchHistory.objects.filter(
            user = user,
            chat_server = chatserver,
            search_text__icontains=search_text
        ).order_by('-created_on')[:10]
        data = [{"search_text": hist.search_text, "created_on": hist.created_on.strftime("%Y-%m-%dT%H:%M:%SZ")} for hist in list_history]

        return {
            "type": "search_history",
            "query": search_text,
            "data": data
        }

    def action_default(self, msg, chatserver, user):
        return {
            "type": "text",
            "data": """
                Sorry! I am unable to understand. If you like to search on google type `!google` followed by search text or
                type `!recent` followed by search query to view your search history.
            """

        }
    # --- /Actions ---


    def process(self, message, chatserver, user):
        """
        Method to process an incoming message.

        :param message: text string
        :param chatserver: Instance of :class:`core.models.ChatServer`
        :param user: Instance of `User` class
        :return: result
        """
        assert message not in ["", None]

        # Preprocess message
        message = message.lower()
        tokens = message.split()

        # Identify the intent
        intent_key = tokens[0]
        if intent_key not in self.INTENTS:
            action_method = self.action_default
        else:
            action_method = self.INTENTS[intent_key]

        # Execute action
        result = action_method(msg=message, chatserver=chatserver, user=user)

        return result




