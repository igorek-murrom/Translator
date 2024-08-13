from django.shortcuts import render


# Create your views here.


def video0(request):
    return render(request, 'videos/video0.html')


def video1(request):
    return render(request, 'videos/video1.html')


def video2(request):
    return render(request, 'videos/video2.html')


def video3(request):
    return render(request, 'videos/video3.html')


def video4(request):
    return render(request, 'videos/video4.html')
