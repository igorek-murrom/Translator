from django.urls import path
from main import views

urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.upload, name='upload_file'),
    path('success/', views.success, name='success'),
    path('start/', views.start, name='start_script'),
    path('stop/', views.stop, name='stop_script'),
    path('showcode/', views.show_code, name='show_code'),
]