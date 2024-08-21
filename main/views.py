from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.conf import settings
import os
import subprocess
from main.forms import UploadFileForm


def index(request):
    return render(request, 'main/index.html')


def upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']
            file_path = os.path.join('sub_python', uploaded_file.name)
            if os.path.exists(file_path):
                os.remove(file_path)

            form.save()
            return redirect('success')
    else:
        form = UploadFileForm()
    return render(request, 'main/upload.html', {'form': form})


def success(request):
    return render(request, 'main/success.html')


def start(request):
    if settings.PROCESS is None:
        settings.PROCESS = subprocess.Popen(['python', 'sub_python/main.py'])
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
    with open('sub_python/main.py', 'r') as file:
        code = file.read()
        return HttpResponse(code, content_type='text/plain')