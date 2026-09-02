# pyrefly: ignore [missing-import]
from django.db import models

# pyrefly: ignore [missing-import]
from django.contrib.auth import get_user_model

User = get_user_model()


class Post(models.Model):
    title_coloum = models.CharField(max_length=100)
    content_coloum = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title_coloum


class PostImage(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="images"
    )
    image = models.ImageField(upload_to="posts/")