# blog/urls.py

from django.urls import path

from . import views

app_name = 'blog'  # namespace: lets us write {% url 'blog:home' %} in templates

urlpatterns = [
    path('', views.home, name='home'),  # '' = root URL (/), name='home' lets us reference it in templates
]