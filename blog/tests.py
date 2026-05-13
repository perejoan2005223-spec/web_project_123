from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Department, Professor, Subject, Prof_Subject, Review


class ReviewCRUDTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='alumne1', password='password123')
        self.other_user = User.objects.create_user(username='alumne2', password='password123')

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
            'comment': "Molt bon professor, s'explica molt bé."
        }

        response = self.client.post(reverse('blog:review_create'), data)
        self.assertRedirects(response, reverse('blog:home'))
        self.assertEqual(Review.objects.count(), 1)

        review = Review.objects.first()
        self.assertEqual(review.comment, "Molt bon professor, s'explica molt bé.")
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

        #Iniciem sessió amb l'usuari propietari
        self.client.login(username='alumne1', password='password123')

        dades_noves = {
            'prof_subject': self.prof_subject.id,
            'overall_rating': 9,
            'difficulty_rating': 8,
            'comment': "He canviat d'opinió, el professor és un duro!"
        }

        response = self.client.post(reverse('blog:review_update', kwargs={'pk': review.pk}), dades_noves)

        self.assertRedirects(response, reverse('blog:professor_detail', kwargs={'pk': self.professor.id}))

        #Actualitzem la nostra variable 'review' amb els fets reals de la base de dades
        review.refresh_from_db()

        #Comprovem que els canvis s'han aplicat correctament
        self.assertEqual(review.comment, "He canviat d'opinió, el professor és un duro!")
        self.assertEqual(review.overall_rating, 9)

    def test_editar_review_altre_usuari(self):
        """Test que impedeix a un usuari editar la ressenya d'un altre."""
        review = Review.objects.create(
            user=self.other_user, #Propietari: alumne2
            prof_subject=self.prof_subject,
            overall_rating=8,
            difficulty_rating=6,
            comment="Aquesta ressenya és meva."
        )

        #Iniciem sessió amb el NO propietari
        self.client.login(username='alumne1', password='password123')

        dades_malicioses = {
            'prof_subject': self.prof_subject.id,
            'overall_rating': 1,
            'difficulty_rating': 1,
            'comment': "Hackejat per l'alumne1"
        }

        #Intentem editar-la
        response = self.client.post(reverse('blog:review_update', kwargs={'pk': review.pk}), dades_malicioses)

        #Comprovem que nomes pot trobar les seves reviews i no les dels demés (404 Not found)
        self.assertEqual(response.status_code, 404)

        #Verifiquem que la ressenya NO ha canviat a la base de dades
        review.refresh_from_db()
        self.assertEqual(review.comment, "Aquesta ressenya és meva.")
        self.assertEqual(review.overall_rating, 8)

    def test_elmininar_ressenya(self):
        """Test per comprovar que un usuari pot esborrar la seva pròpia ressenya."""

        review = Review.objects.create(
            user=self.user,
            prof_subject=self.prof_subject,
            overall_rating=7,
            difficulty_rating=5,
            comment="Aquesta ressenya serà esborrada."
        )
        #Comprovar que s'ha creat
        self.assertEqual(Review.objects.count(), 1)

        self.client.login(username='alumne1', password='password123')
        response = self.client.post(reverse('blog:review_delete', kwargs={'pk': review.pk}))

        self.assertRedirects(response, reverse('blog:professor_detail', kwargs={'pk': self.professor.id}))

        # 5. Comprovem que la ressenya JA NO existeix a la base de dades
        self.assertEqual(Review.objects.count(), 0)

    def test_esborrar_review_altre_usuari(self):
        """Test que impedeix a un usuari esborrar la ressenya d'un altre."""

        review = Review.objects.create(
            user=self.other_user,  #Propietari: alumne2
            prof_subject=self.prof_subject,
            overall_rating=8,
            difficulty_rating=4,
            comment="Ressenya d'un altre."
        )

        #Iniciem sessió amb el NO propietari
        self.client.login(username='alumne1', password='password123')

        response = self.client.post(reverse('blog:review_delete', kwargs={'pk': review.pk}))

        #Comprovem que nomes pot trobar les seves reviews i no les dels demés (404 Not found)
        self.assertEqual(response.status_code, 404)

        #Comprovem que la ressenya SEGUEIX a la base de dades
        self.assertEqual(Review.objects.count(), 1)