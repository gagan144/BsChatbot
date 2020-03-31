from django.contrib import admin

from core.models import *


@admin.register(ChatServer)
class ChatServerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'user', 'created_on', 'modified_on')
    search_fields = ('name', )
    date_hierarchy = 'created_on'

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = self.readonly_fields + tuple(field.name for field in self.model._meta.fields if field.editable==False)
        return readonly_fields


@admin.register(SearchHistory)
class SearchHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'chat_server', 'search_text', 'created_on')
    search_fields = ('search_text',)
    list_filter = ('chat_server',)
    date_hierarchy = 'created_on'

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = self.readonly_fields + tuple(field.name for field in self.model._meta.fields if field.editable==False)
        return readonly_fields
