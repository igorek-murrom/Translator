from django.apps import AppConfig


def get_cmd() -> list:
    import shlex
    cmd = open("sub/command.txt", 'r')
    command = shlex.split(cmd.read())
    cmd.close()
    return command


class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'

    def ready(self):
        from django.conf import settings
        import subprocess
        import os
        import threading
        from main import servers

        try:
            if os.path.exists(settings.SUB_DIR):
                files = os.listdir(settings.SUB_DIR)
                if 'autostart.txt' in files:
                    autostart_file = open(settings.SUB_DIR + 'autostart.txt', 'r')
                    status = autostart_file.read()
                    autostart_file.close()
                    if status == 'True':
                        print('AUTOSTART')
                        settings.PROCESS = subprocess.Popen(get_cmd())
        except:
            print("error in autostart")

        websocket_thread = threading.Thread(target=servers.start_websocket)
        socket_thread = threading.Thread(target=servers.start_socket)

        websocket_thread.start()
        socket_thread.start()