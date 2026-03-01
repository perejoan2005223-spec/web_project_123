# web_project/urls.py
from django.contrib import admin
from django.urls import include, path  # Importante añadir 'include' aquí

urlpatterns = [
    path('admin/', admin.site.urls),   # Panel de administración predeterminado
    path('', include('blog.urls')),    # Reenvía las peticiones a blog/urls.py
]