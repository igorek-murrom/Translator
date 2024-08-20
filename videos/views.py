from django.shortcuts import render


def video1(request):
    return render(request, 'videos/video.html', {'number': 1})


def video2(request):
    return render(request, 'videos/video.html', {'number': 2})


def video3(request):
    return render(request, 'videos/video.html', {'number': 3})


def video4(request):
    return render(request, 'videos/video.html', {'number': 4})


def video5(request):
    return render(request, 'videos/video.html', {'number': 5})