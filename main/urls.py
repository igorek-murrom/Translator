from django.urls import path
from main import views

urlpatterns = [
    path('', views.index, name='index'),

    path('upload/', views.upload, name='upload_file'),
    path('success/', views.success, name='success'),

    path('start/', views.start, name='start_script'),
    path('stop/', views.stop, name='stop_script'),

    path('showcode/', views.show_code, name='show_code'),
    path('status/', views.show_status, name='show_status'),
    path('editscript/', views.edit_script, name='edit_script'),

    path('keyboard/', views.keyboard_view, name='keyboard_view'),
    path('handle_keypress/', views.handle_keypress, name='handle_keypress'),

    path('video/<int:number>/', views.video, name='video'),
]