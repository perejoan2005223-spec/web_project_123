# blog/views.py
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView # generic views that handle common patterns

from .models import Professor

def home(request):
    """Home page view."""
    # request = the incoming HTTP request (URL, method, headers, user info, etc.)
    # render() loads the template file, returns it as an HTTP response
    return render(request, 'blog/home.html')


class PostSignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

# All professor list
class ProfessorListView(ListView):
    model = Professor
    template_name = 'blog/professor_list.html'
    context_object_name = 'professors'

# Professor profile
class ProfessorDetailView(DetailView):
    model = Professor
    template_name = 'blog/professor_detail.html'
    context_object_name = 'professor'