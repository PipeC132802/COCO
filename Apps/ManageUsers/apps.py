from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'Apps.ManageUsers'

    def ready(self):
        import Apps.ManageUsers.signals
