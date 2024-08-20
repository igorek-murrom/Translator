from django.urls import path
from . import views

urlpatterns = [
    path('video/1', views.video1, name='video1'),
    path('video/2', views.video2, name='video2'),
    path('video/3', views.video3, name='video3'),
    path('video/4', views.video4, name='video4'),
    path('video/5', views.video4, name='video5'),

]
