from django.contrib import admin
from django.urls import path
from main import urls as main_urls

urlpatterns = [
                  path('admin/', admin.site.urls, name='admin'),
              ] + main_urls.urlpatterns
