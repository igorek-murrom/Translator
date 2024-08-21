from django.apps import AppConfig


class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'

    def ready(self):
        from django.conf import settings
        import subprocess
        try:
            from sub_python.main import API_AUTOSTART
            if API_AUTOSTART:
                settings.PROCESS = subprocess.Popen(['python', 'sub_python/main.py'])
                print('AUTOSTART')
        except ImportError:
            print("dont find API_AUTOSTART")
