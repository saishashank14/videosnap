# pyrefly: ignore [missing-import]
from django.urls import path
from . import views

urlpatterns = [
    path("allpost/", views.posts_view, name="allpost"),
    path("create_post/", views.create_post_view, name="create_post"),
]