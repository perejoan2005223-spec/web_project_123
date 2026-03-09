# blog/admin.py

from django.contrib import admin

from .models import Post


@admin.register(Post)  # register Post in Django's admin panel
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')  # columns shown in the post list
    list_filter = ('author', 'created_at')             # sidebar filters
    search_fields = ('title', 'body')                  # searchable fields