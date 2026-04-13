# blog/admin.py

from django.contrib import admin
from .models import Department, Professor, Title, Subject, Prof_Subject, Publication, Professor_Publication, Review

# Registramos los nuevos modelos para poder verlos y editarlos en el panel de Admin de Django.
admin.site.register(Department)
admin.site.register(Professor)
admin.site.register(Title)
admin.site.register(Subject)
admin.site.register(Prof_Subject)
admin.site.register(Publication)
admin.site.register(Professor_Publication)
admin.site.register(Review)