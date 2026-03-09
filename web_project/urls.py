# DjangoProject/urls.py

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),  # all of Django's auth views (login, logout, etc.)
    path('', include('blog.urls')),
]