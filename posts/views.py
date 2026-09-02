# pyrefly: ignore [missing-import]
from django.shortcuts import render, redirect
from .models import Post, PostImage


# Display all posts
def posts_view(request):
    posts = Post.objects.all()     #all rows or all data from models
    return render(request, "accounts/allpost.html", {"allpost": posts})


# Create a new post
def create_post_view(request):

    if request.method == "POST":
        title = request.POST.get("title_html")
        content = request.POST.get("content_html")

        # Create the post
        post = Post.objects.create(
            title_coloum=title,
            content_coloum=content
        )

        # Get all uploaded images
        images = request.FILES.getlist("images")

        # Save each image
        for image in images:
            PostImage.objects.create(
                post=post,
                image=image
            )

        return redirect("allpost")

    return render(request, "accounts/create_post.html")