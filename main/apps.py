from django.apps import AppConfig


class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'

    def ready(self):
        from django.conf import settings
        try:
            autostart_status = settings.PROCESS.get_autostart_status()
            if autostart_status:
                settings.PROCESS.start()
        except:
            print("error in autostart")
