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
    if settings.PROCESS is None:
        settings.PROCESS = subprocess.Popen(['python', settings.SUB_DIR + 'main.py'])
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
    if not os.path.exists(settings.SUB_DIR): return JsonResponse({'status': 'no code'})

    code = ""
    names = os.listdir(settings.SUB_DIR)
    for f in names:
        if f == "__pycache__": continue
        code += "########## " + f + " ##########" + "\n"
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