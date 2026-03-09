# blog/urls.py

from django.urls import path

from . import views

app_name = 'blog'  # namespace: lets us write {% url 'blog:home' %} in templates

urlpatterns = [
    path('', views.home, name='home'),  # '' = root URL (/), name='home' lets us reference it in templates
    path('posts/', views.PostListView.as_view(), name='post_list'),        # .as_view() turns the class into a callable view
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),  # <int:pk> captures the post ID from the URL
]