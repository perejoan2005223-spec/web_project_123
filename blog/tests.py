from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Department, Professor, Subject, Prof_Subject, Review


class ReviewCRUDTests(TestCase):

    def setUp(self):
        # 1. Creem els usuaris de prova necessaris per a l'autenticació
        self.user = User.objects.create_user(username='alumne1', password='password123')
        self.other_user = User.objects.create_user(username='alumne2', password='password123')

        # 2. Creem les dades de l'entorn segons els models del projecte
        self.department = Department.objects.create(name_dept="Enginyeria Informàtica")
        self.professor = Professor.objects.create(
            department=self.department,
            name_prof="Dr. Jordi Gómez"
        )
        self.subject = Subject.objects.create(
            name_sub="Enginyeria del Programari",
            description="Assignatura de projectes",
            credits=6
        )
        self.prof_subject = Prof_Subject.objects.create(
            professor=self.professor,
            subject=self.subject,
            year=2026
        )

    def test_crear_review_autenticat(self):
        """Test de creació d'una ressenya."""
        self.client.login(username='alumne1', password='password123')

        data = {
            'prof_subject': self.prof_subject.id,
            'overall_rating': 8,
            'difficulty_rating': 6,
            'comment': 'Molt bon professor, s’explica molt bé.'
        }

        response = self.client.post(reverse('blog:review_create'), data)
        self.assertRedirects(response, reverse('blog:home'))
        self.assertEqual(Review.objects.count(), 1)

        review = Review.objects.first()
        self.assertEqual(review.comment, 'Molt bon professor, s’explica molt bé.')
        self.assertEqual(review.user, self.user)

    def test_crear_review_anonim(self):
        """Test que impedeix crear ressenyes sense login."""
        data = {
            'prof_subject': self.prof_subject.id,
            'overall_rating': 9,
            'difficulty_rating': 4,
            'comment': 'Anònim no hauria de poder.'
        }
        response = self.client.post(reverse('blog:review_create'), data)
        self.assertIn('/login/', response.url)
        self.assertEqual(Review.objects.count(), 0)

    def test_editar_propia_review(self):
        """Test de modificació de la pròpia ressenya."""
        review = Review.objects.create(
            user=self.user,
            prof_subject=self.prof_subject,
            overall_rating=7,
            difficulty_rating=5,
            comment="Comentari original"
        )

        self.client.login(username='alumne1', password='password123')

        updated_data = {
            'prof_subject': self.prof_subject.id,
            'overall_rating': 9,
            'difficulty_rating': 5,
            'comment': "Comentari modificat"
        }

        # S'utilitza la ruta de creació o edició segons correspongui
        response = self.client.post(reverse('blog:review_create'), updated_data)
        review.refresh_from_db()

    def test_eliminar_propia_review(self):
        """Test per esborrar una ressenya existent."""
        review = Review.objects.create(
            user=self.user,
            prof_subject=self.prof_subject,
            overall_rating=6,
            difficulty_rating=6,
            comment="Això s'eliminarà"
        )

        self.client.login(username='alumne1', password='password123')
        Review.objects.filter(pk=review.pk).delete()
        self.assertEqual(Review.objects.count(), 0)