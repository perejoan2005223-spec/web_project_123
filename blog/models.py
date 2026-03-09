# blog/models.py

from django.contrib.auth.models import User  # Django's built-in user model
from django.db import models
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(max_length=200)  # short text, max 200 chars
    body = models.TextField()  # long text, no limit
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # link to User; CASCADE = delete posts if user deleted
    created_at = models.DateTimeField(auto_now_add=True)  # auto-set when created

    class Meta:
        ordering = ['-created_at']  # default sort: newest first ('-' = descending)

    def __str__(self):
        return self.title  # shown in admin panel and Django shell

    def get_absolute_url(self):
        # Returns this post's URL (e.g. /posts/3/)
        # Django calls this automatically to redirect after creating a post
        return reverse('blog:post_detail', kwargs={'pk': self.pk})
