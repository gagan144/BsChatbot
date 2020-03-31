from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class ChatServer(models.Model):
    """
    Model to store chat server.
    """
    name    = models.SlugField(max_length=50, unique=True, db_index=True, help_text='Unique name of the server.')
    user    = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True, help_text='User that created this server.')

    created_on = models.DateTimeField(auto_now_add=True, editable=False, help_text='Timestamp at which this record was created.')
    modified_on = models.DateTimeField(null=True, blank=True, editable=False, help_text='TImestamp at which this record was last modified.')

    class Meta:
        verbose_name = 'Chat Server'
        verbose_name_plural = 'Chat Servers'

    def __str__(self):
        return self.name

    def clean(self):
        """
        Method to clean & validate fields.
        """
        if self.pk:
            self.modified_on = timezone.now()

        super(self.__class__, self).clean()

    def save(self, *args, **kwargs):
        """
        Pre-save method for this model.
        """
        self.clean()
        super(self.__class__, self).save(*args, **kwargs)



class SearchHistory(models.Model):
    """
    Model to store user's search history.
    """
    user    = models.ForeignKey(User, on_delete=models.NullBooleanField, db_index=True, help_text='User for which history is recorded.')
    chat_server = models.ForeignKey(ChatServer, on_delete=models.NullBooleanField, db_index=True, help_text='Chat server where search was made.')

    search_text = models.CharField(max_length=255, db_index=True, help_text='Search query text.')

    created_on = models.DateTimeField(auto_now_add=True, editable=False, help_text='Timestamp at which this record was created.')

    class Meta:
        verbose_name = 'Search History'
        verbose_name_plural = 'Search Histories'

    def __str__(self):
        return "{} - {}".format(self.id, self.search_text)


