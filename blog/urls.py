# blog/urls.py
from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.PostSignUpView.as_view(), name='signup'),
    path('profesores/', views.ProfessorListView.as_view(), name='professor_list'),
    path('profesores/<int:pk>/', views.ProfessorDetailView.as_view(), name='professor_detail'),

    # Rutes del CRUD de Review
    path('review/nova/', views.ReviewCreateView.as_view(), name='review_create'),
]