# blog/models.py

from django.db import models
from django.contrib.auth.models import User  # Use django's integrated user
from django.core.validators import MinValueValidator, MaxValueValidator

#Also, the PK (id) is set automatically by django

class Department(models.Model):
    name_dept = models.CharField(max_length=100)

    def __str__(self):
        return self.name_dept


class Professor(models.Model):
    # FK department Relation 1..*
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='professors')
    name_prof = models.CharField(max_length=150)
    profile_pic_url = models.URLField(max_length=200, blank=True, null=True)  #URLField for links

    def __str__(self):
        return self.name_prof



class Title(models.Model):
    #1 prof can can have * titles
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE, related_name='titles')
    category = models.CharField(max_length=100)
    expedition_date = models.DateField()

    def __str__(self):
        return f"{self.category} - {self.professor.name_prof}"


class Subject(models.Model):
    name_sub = models.CharField(max_length=150)
    description = models.TextField()
    credits = models.PositiveIntegerField()

    #Many-to-many relation, passing through Prof_Subject
    #Because of related_name, the relation is bidirectioal, ex: my_profesor.subjects.all()
    professors = models.ManyToManyField(Professor, through='Prof_Subject', related_name='subjects')

    def __str__(self):
        return self.name_sub


# Classe de associació
class Prof_Subject(models.Model):
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    year = models.IntegerField()

    def __str__(self):
        return f"{self.professor.name_prof} - {self.subject.name_sub} ({self.year})"


class Publication(models.Model):
    title_pub = models.CharField(max_length=200)
    publish_year = models.PositiveIntegerField()
    url = models.URLField(max_length=200)

    #Many-to-many relation, passing through Professor_Publication
    authors = models.ManyToManyField(Professor, through='Professor_Publication', related_name='publications')

    def __str__(self):
        return self.title_pub


# Classe d'associació
class Professor_Publication(models.Model):
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)
    author_order = models.PositiveIntegerField()  # Per indicar si és el 1er autor, 2on autor...

    class Meta:
        ordering = ['author_order']  # Ordena por defecto por el orden de autoría

    def __str__(self):
        return f"{self.professor.name_prof} - {self.publication.title_pub}"


class Review(models.Model):
    # A User makes the review over a specific Prof_Subject
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    prof_subject = models.ForeignKey(Prof_Subject, on_delete=models.CASCADE, related_name='reviews')

    # Validators to make the marks between 0 and 10
    overall_rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    difficulty_rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    comment = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)  #The current date-time is set automatically

    def __str__(self):
        return f"Review de {self.user.username} para {self.prof_subject}"