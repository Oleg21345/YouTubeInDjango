from django.contrib import admin
from youtube.models import Video
# Register your models here.

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ("title", "desc", "create_at", "autor")
    readonly_fields = ("slug", "title", "desc", "create_at", "autor",
                       "is_published","watch", "like", "dislike",
                       "url_photo", "url_video", "url_video_240", "url_video_360", "url_video_720", "url_video_1080")

