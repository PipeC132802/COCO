from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'ManageUsers'

    def ready(self):
        import Apps.ManageUsers.signals
