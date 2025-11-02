from django.contrib import admin
from youtube.models import Video, PlayList,LikesVideo, Autor,WatchLater,Vote, Notificated
# Register your models here.

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ("title", "desc", "create_at", "autor")
    readonly_fields = ("slug", "title", "desc", "create_at", "autor",
                       "is_published","watch",
                       "url_photo", "url_video", "url_video_240", "url_video_360", "url_video_720", "url_video_1080")
    search_fields = ("title", "autor__username", "slug")


@admin.register(PlayList)
class PlayListAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "access", "slug")
    search_fields = ("name", "user__username")
    list_filter = ("access",)
    filter_horizontal = ("videos",)
    readonly_fields = ("slug", "user")
    prepopulated_fields = {}

    def has_change_permission(self, request, obj=None):
        if obj and not request.user.is_superuser:
            return True
        return super().has_change_permission(request, obj)


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ("user", "video", "value")
    list_filter = ("value",)
    search_fields = ("user__username", "video__title")
    autocomplete_fields = ("user", "video")
    readonly_fields = ("user", "video")

    def has_add_permission(self, request):
        return False


@admin.register(Notificated)
class NotificatedAdmin(admin.ModelAdmin):
    list_display = ("user", "from_user", "notificated_preview", "is_read", "notificated_count", "create_at")
    list_filter = ("is_read", "create_at")
    search_fields = ("user__username", "from_user__username", "notificated")
    readonly_fields = ("user", "from_user", "create_at", "notificated_count")

    def notificated_preview(self, obj):
        return obj.notificated[:50]
    notificated_preview.short_description = "Notification text"

    def has_add_permission(self, request):
        return False


@admin.register(WatchLater)
class WatchLaterAdmin(admin.ModelAdmin):
    list_display = ("user", "video", "count_watch", "added_at")
    list_filter = ("added_at",)
    search_fields = ("user__username", "video__title")
    autocomplete_fields = ("user", "video")
    readonly_fields = ("user", "video", "added_at", "count_watch")

    def has_add_permission(self, request):
        return False

@admin.register(LikesVideo)
class LikesVideoAdmin(admin.ModelAdmin):
    list_display = ("user", "video", "count_likes", "added_at")
    search_fields = ("user__username", "video__title")
    readonly_fields = ("count_likes", "added_at")
    autocomplete_fields = ("user", "video")
    list_filter = ("added_at",)