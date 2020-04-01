from django.forms import ModelForm

from core.models import ChatServer


class ChatServerForm(ModelForm):
    """
    Form to create ChatServer instance
    """

    class Meta:
        model = ChatServer
        fields = ['name', 'user']

    def clean(self):
        form_data = self.cleaned_data

        if self.instance.pk is None:
            if ChatServer.objects.filter(name=form_data['name']).exists():
                self._errors["name"] = ["Chat Server with name '{}' already exists.".format(form_data['name'])]

        return form_data