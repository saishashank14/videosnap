from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class VideoCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Video Categories"

    def __str__(self):
        return self.name

class VideoTag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"#{self.name}"

class Video(models.Model):
    uploader = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_videos', null=True, blank=True)
    category = models.ForeignKey(VideoCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='videos')
    tags = models.ManyToManyField(VideoTag, blank=True, related_name='videos')
    title = models.CharField(max_length=200)
    description = models.TextField()
    video = models.FileField(upload_to='videos/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class VideoLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='video_likes')
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'video')

    def __str__(self):
        return f"{self.user.username} liked {self.video.title}"

class VideoComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='video_comments')
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.video.title}"

class VideoShare(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='video_shares')
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='shares')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} shared {self.video.title}"

class VideoView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='video_views', null=True, blank=True)
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='views')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        user_str = self.user.username if self.user else "Anonymous"
        return f"View by {user_str} on {self.video.title}"

class Playlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='playlists')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    videos = models.ManyToManyField(Video, blank=True, related_name='in_playlists')
    is_private = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} by {self.user.username}"

class SavedVideo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_videos')
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='saved_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'video')

    def __str__(self):
        return f"{self.user.username} saved {self.video.title}"

class VideoReport(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('reviewed', 'Reviewed'),
        ('resolved', 'Resolved'),
        ('dismissed', 'Dismissed'),
    )
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='video_reports')
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='reports')
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report on {self.video.title} by {self.reporter.username}"
# Create your models here.
