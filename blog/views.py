# blog/views.py
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.views.generic import CreateView, ListView, DetailView # generic views that handle common patterns
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Professor, Review
from django import forms
from django.http import JsonResponse

def professor_autocomplete(request):
    query = request.GET.get('term', '')
    professors = Professor.objects.filter(name_prof__icontains=query)
    results = [{'label': p.name_prof, 'value': p.name_prof, 'url': f'/profesores/{p.pk}/'} for p in professors]
    return JsonResponse(results, safe=False)

def home(request):
    """Home page view."""
    # request = the incoming HTTP request (URL, method, headers, user info, etc.)
    # render() loads the template file, returns it as an HTTP response
    return render(request, 'blog/home.html')


class PostSignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

# Llista de tots els professors
class ProfessorListView(ListView):
    model = Professor
    template_name = 'blog/professor_list.html'
    context_object_name = 'professors'

# Perfil del professor
class ProfessorDetailView(DetailView):
    model = Professor
    template_name = 'blog/professor_detail.html'
    context_object_name = 'professor'

# Estructura de la ressenya + límits de la valoració
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['prof_subject', 'overall_rating', 'difficulty_rating', 'comment']

        # Perquè es vegi en català
        labels = {
            'prof_subject': 'Assignatura i Professor',
            'overall_rating': 'Nota Global',
            'difficulty_rating': 'Dificultat',
            'comment': 'Comentari',
        }

        widgets = {
            'overall_rating': forms.NumberInput(attrs={'min': '0', 'max': '10'}),
            'difficulty_rating': forms.NumberInput(attrs={'min': '0', 'max': '10'}),
            'comment': forms.Textarea(attrs={'rows': 5}),
        }

# Lògica de les ressenyes
class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    # No incloem 'user' als camps perquè l'assignarem automàticament
    template_name = 'blog/review_form.html'
    success_url = reverse_lazy('blog:home')

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
