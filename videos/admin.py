from django.contrib import admin
from .models import (
    VideoCategory, VideoTag, Video, VideoLike, VideoComment,
    VideoShare, VideoView, Playlist, SavedVideo, VideoReport
)

admin.site.register(VideoCategory)
admin.site.register(VideoTag)
admin.site.register(Video)
admin.site.register(VideoLike)
admin.site.register(VideoComment)
admin.site.register(VideoShare)
admin.site.register(VideoView)
admin.site.register(Playlist)
admin.site.register(SavedVideo)
admin.site.register(VideoReport)
# Register your models here.
