# blog/views.py
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.views.generic import CreateView, ListView, DetailView # generic views that handle common patterns
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Professor, Review

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


class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    # No incloem 'user' als camps perquè l'assignarem automàticament
    fields = ['prof_subject', 'overall_rating', 'difficulty_rating', 'comment']
    template_name = 'blog/review_form.html'
    success_url = reverse_lazy('blog:home') # O redirigeix on prefereixis

    def get_initial(self):
        # Agafem les dades inicials per defecte
        initial = super().get_initial()
        # Si a la URL hi ha un paràmetre 'prof_subject', el posem com a valor inicial del camp
        prof_subject_id = self.request.GET.get('prof_subject')
        if prof_subject_id:
            initial['prof_subject'] = prof_subject_id
        return initial

    def form_valid(self, form):
        # Assignem l'usuari actual abans de guardar la instància a la base de dades
        form.instance.user = self.request.user
        return super().form_valid(form)

class ReviewUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Review
    fields = ['overall_rating', 'difficulty_rating', 'comment'] # L'usuari no hauria de poder canviar l'assignatura
    template_name = 'blog/review_form.html'
    success_url = reverse_lazy('blog:home')

    def test_func(self):
        # Aquesta funció comprova si l'usuari és el propietari.
        # Si retorna False, Django denegarà l'accés (Error 403).
        review = self.get_object()
        return self.request.user == review.user

class ReviewDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Review
    template_name = 'blog/review_confirm_delete.html'
    success_url = reverse_lazy('blog:home')

    def test_func(self):
        # Mateixa comprovació: només el creador pot eliminar
        review = self.get_object()
        return self.request.user == review.user