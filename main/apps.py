from django.apps import AppConfig


class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'

    def ready(self):
        from django.conf import settings
        import subprocess
        import os
        try:
            if os.path.exists(settings.SUB_DIR):
                files = os.listdir(settings.SUB_DIR)
                if 'main.py' in files and 'autostart.txt' in files:
                    autostart_file = open(settings.SUB_DIR + 'autostart.txt', 'r')
                    status = autostart_file.read()
                    autostart_file.close()
                    if status == 'True':
                        settings.PROCESS = subprocess.Popen(['python', settings.SUB_DIR + 'main.py'])
                        print('AUTOSTART')
        except:
            print("error in autostart")
