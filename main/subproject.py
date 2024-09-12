import subprocess
import threading
import shlex
import os
from django.conf import settings


def get_cmd() -> list:
    with open(os.path.join('sub', 'command.txt'), 'r') as cmd:
        command = shlex.split(cmd.read())
    return command


class SubProgram:
    def __init__(self):
        self.process = None
        self.monitor_thread = None

    def start(self) -> bool:
        if self.process is not None:
            return False
        self.process = subprocess.Popen(get_cmd(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=settings.SUB_DIR)
        print(self.process)
        self.monitor_thread = threading.Thread(target=self.monitor_process)
        self.monitor_thread.start()
        return True

    def stop(self) -> bool:
        if self.is_running():
            self.process.terminate()
            self.process.wait()
            self.process = None
            return True
        else:
            return False

    def is_running(self) -> bool:
        return self.process is not None

    def get_autostart_status(self):
        if os.path.exists(settings.SUB_DIR):
            files = os.listdir(settings.SUB_DIR)
            if 'autostart.txt' in files:
                with open(os.path.join(settings.SUB_DIR, 'autostart.txt'), 'r') as autostart_file:
                    status = autostart_file.read()
                if status == "True":
                    return True
        return False

    def monitor_process(self):
        if self.is_running():
            try:
                stdout, stderr = self.process.communicate()
                print(f"Program output:\n{stdout}")
                if stderr:
                    print(f"Program errors:\n{stderr}")
                with open(os.path.join('sub', 'output.txt'), 'w') as f:
                    f.write(stdout)
                    f.write(stderr)
            except Exception as e:
                print(f"Error while running the program: {e}")
            finally:
                if self.is_running(): self.stop()
                print("Process terminated")

            if self.is_running(): self.stop()
