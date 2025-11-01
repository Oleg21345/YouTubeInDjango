from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.urls import reverse
import uuid
# Create your models here.



class Autor(models.Model):
    slug = models.SlugField(default=str(uuid.uuid4())[:8])
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="autor")
    avatar = models.URLField(max_length=500)
    pseudonym = models.CharField(max_length=100, blank=True, null=True)
    nickname = models.CharField(max_length=100, unique=True, blank=True, null=True)
    desc = models.TextField(max_length=600, blank=True, null=True)
    data = models.DateField(blank=True, null=True)
    subscriptions = models.IntegerField(default=0)
    subscribers = models.IntegerField(default=0)
    photo = models.ImageField(upload_to='autors/photos/', blank=True, null=True)
    banner = models.ImageField(upload_to='autors/banners/', blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)

    def __str__(self):
        return f"{self.nickname}"



class Video(models.Model):
    slug = models.SlugField(default=str(uuid.uuid4())[:8])
    title = models.CharField(max_length=150)
    desc = models.CharField(max_length=600)
    create_at = models.DateTimeField(auto_now=True)
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="video")
    is_published = models.BooleanField(default=False)
    watch = models.IntegerField(default=0)
    url_photo = models.URLField(max_length=500)
    url_video = models.URLField()
    url_video_240 = models.URLField(blank=True, null=True)
    url_video_360 = models.URLField(blank=True, null=True)
    url_video_720 = models.URLField(blank=True, null=True)
    url_video_1080 = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title

    @property
    def like_count(self):
        return self.votes.filter(value=1).count()

    @property
    def dislike_count(self):
        return self.votes.filter(value=-1).count()



class Vote(models.Model):
    VOTE_CHOICE = (
        (1, "like"),
        (-1, "dislike")
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="votes")
    value = models.SmallIntegerField(choices=VOTE_CHOICE)

    class Meta:
        unique_together = ('user', 'video')


class Notificated(models.Model):
    user = models.ForeignKey(User, related_name="user_notif", on_delete=models.CASCADE)
    notificated = models.TextField()
    from_user = models.ForeignKey(User, related_name="sent_notifications", null=True, blank=True, on_delete=models.SET_NULL)
    is_read = models.BooleanField(default=False)
    notificated_count = models.IntegerField()
    create_at = models.DateTimeField(auto_now_add=True, verbose_name="Data")

    def __str__(self):
        return f"Notification for {self.user.username}: {self.notificated[:20]}"


class WatchLater(models.Model):
    user = models.ForeignKey(User, related_name="user_video", on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    count_watch = models.IntegerField(default=0)
    added_at = models.DateTimeField(auto_now_add=True, verbose_name="Data")

    class Meta:
        unique_together = ("user", "video")
        ordering = ["-added_at"]

    def __str__(self):
        return f"{self.user.username} → {self.video.title}"


class LikesVideo(models.Model):
    user = models.ForeignKey(User, related_name="likeu_video", on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    count_likes = models.IntegerField(default=0)
    added_at = models.DateTimeField(auto_now_add=True, verbose_name="Data")

    def __str__(self):
        return self.count_likes


