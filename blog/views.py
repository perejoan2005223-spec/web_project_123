# blog/views.py
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.views.generic import DetailView, ListView, CreateView  # generic views that handle common patterns

from .models import Post

def home(request):
    """Home page view."""
    # request = the incoming HTTP request (URL, method, headers, user info, etc.)
    # render() loads the template file, returns it as an HTTP response
    return render(request, 'blog/home.html')

class PostListView(ListView):
    model = Post                           # which table to query
    template_name = 'blog/post_list.html'  # which template to render
    context_object_name = 'posts'          # variable name in the template (default would be 'object_list')

class PostDetailView(DetailView):
    model = Post                            # which table to query
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'    # variable name in the template (default would be 'object')


class PostSignUpView(CreateView):
    form_class = UserCreationForm
    success_url = '/login/'
    template_name = 'blog/signup.html'