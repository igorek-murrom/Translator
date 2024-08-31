import os
import shutil
import subprocess

from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect

from main.forms import UploadFileForm


def index(request):
    return render(request, 'main/index.html')


def upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            if os.path.exists(settings.SUB_DIR):
                shutil.rmtree(settings.SUB_DIR)
            os.mkdir(settings.SUB_DIR)

            files = form.cleaned_data["file_field"]
            for f in files:
                fh = open(settings.SUB_DIR + str(f), 'ab')
                fh.write(f.read())
                fh.close()
            return redirect('success')
    else:
        form = UploadFileForm()
    return render(request, 'main/upload.html', {'form': form})


def success(request):
    return render(request, 'main/success.html')


def start(request):
    def get_cmd() -> list:
        import shlex
        cmd = open("sub/command.txt", 'r')
        command = shlex.split(cmd.read())
        cmd.close()
        return command

    if settings.PROCESS is None:
        settings.PROCESS = subprocess.Popen(get_cmd())
        print(settings.PROCESS)
        return JsonResponse({'status': 'started'})
    else:
        return JsonResponse({'status': 'already started'})


def stop(request):
    if settings.PROCESS is not None:
        settings.PROCESS.terminate()
        settings.PROCESS = None
        return JsonResponse({'status': 'stopped'})
    else:
        return JsonResponse({'status': 'not running'})


def show_code(request):
    def get_name(ln: int, name: str, cnt: int) -> str:
        ans = ""
        diff = ln - len(name)
        ans += (cnt + diff // 2) * '#' + ' '
        ans += name
        if diff % 2 != 0: ans += ' '
        ans += ' ' + (cnt + diff // 2) * '#' + '\n'
        return ans

    if not os.path.exists(settings.SUB_DIR): return JsonResponse({'status': 'no code'})

    code = ""
    names = os.listdir(settings.SUB_DIR)
    len_name = len(sorted(names, key=len, reverse=True)[0])
    for f in names:
        if f == "__pycache__": continue
        code += get_name(len_name, f, len_name * 2)
        file = open(settings.SUB_DIR + str(f), 'r')
        try:
            code += str(file.read())
        except UnicodeDecodeError:
            code += "error while reading file"
        file.close()
        code += '\n\n'
    return HttpResponse(code, content_type='text/plain')


def show_status(request):
    if settings.PROCESS is None: return JsonResponse({'status': 'not running'})
    return JsonResponse({'status': 'running'})


# views.py
from django.shortcuts import render, redirect
from django.http import HttpResponse
import os


def edit_script(request):
    file_path = os.path.join('sub', 'command.txt')

    if request.method == 'POST':
        new_command = request.POST.get('command')
        with open(file_path, 'w') as file:
            file.write(new_command)
        return redirect('edit_script')

    with open(file_path, 'r') as file:
        command = file.read()

    return render(request, 'main/edit_script.html', {'command': command})
