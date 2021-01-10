from django.apps import AppConfig
class BartersConfig(AppConfig):
    name = 'Apps.ManageBarters'

    def ready(self):
        import Apps.ManageBarters.signals
