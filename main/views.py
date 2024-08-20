from django.shortcuts import render, redirect
from .forms import UploadFileForm
import os
import subprocess
from django.http import JsonResponse, HttpResponse


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


process = None


def start(request):
    global process
    if process is None:
        process = subprocess.Popen(['python', 'sub_python/main.py'])
        return JsonResponse({'status': 'started'})
    else:
        return JsonResponse({'status': 'already running'})


def stop(request):
    global process
    if process is not None:
        process.terminate()
        process = None
        return JsonResponse({'status': 'stopped'})
    else:
        return JsonResponse({'status': 'not running'})


def show_code(request):
    with open('sub_python/main.py', 'r') as file:
        code = file.read()
        return HttpResponse(code, content_type='text/plain')