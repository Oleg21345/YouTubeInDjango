from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.urls import reverse
import uuid
# Create your models here.


def generate_random_slug():
    return uuid.uuid4().hex[:8]

class Autor(models.Model):
    slug = models.SlugField(unique=True, null=True, blank=True, default=generate_random_slug)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="autor")
    avatar = models.URLField(max_length=500)
    pseudonym = models.CharField(max_length=100, blank=True, null=True)
    nickname = models.CharField(max_length=100, unique=True, blank=True, null=True)
    desc = models.TextField(max_length=600, blank=True, null=True)
    data = models.DateField(blank=True, null=True)
    subscribers = models.ManyToManyField(User, related_name="following", blank=True)
    subscriptions = models.ManyToManyField(User, related_name="follow", blank=True)
    photo = models.ImageField(upload_to='autors/photos/', blank=True, null=True)
    banner = models.ImageField(upload_to='autors/banners/', blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)

    def __str__(self):
        return f"{self.nickname}"

    def subscriber_count(self):
        return self.subscribers.count()

    def subscription_count(self):
        return self.subscriptions.count()


class Video(models.Model):
    slug = models.SlugField(unique=True, null=True, blank=True, default=generate_random_slug)
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


class PlayList(models.Model):
    ACCESS_CHOICES = (
        (1, "Public"),
        (2, "Unlisted"),
        (3, "Private"),
    )

    slug = models.SlugField(unique=True, null=True, blank=True, default=generate_random_slug)
    name = models.CharField(max_length=150,)
    access = models.IntegerField(choices=ACCESS_CHOICES, default=3)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    videos = models.ManyToManyField(Video, blank=True, related_name="playlist")



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
        return str(self.count_likes)

class CommentsVideo(models.Model):
    slug = models.SlugField(unique=True, null=True, blank=True, default=generate_random_slug)
    user = models.ForeignKey(User, related_name="user_coment", on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    reply_to_comment = models.ForeignKey("self", on_delete=models.CASCADE, blank=True, null=True,related_name='replies')
    text = models.TextField(max_length=1500)
    create_at = models.DateTimeField(auto_now_add=True)

    @property
    def like_count(self):
        return self.votes.filter(value=1).count()

    @property
    def dislike_count(self):
        return self.votes.filter(value=-1).count()

    def __str__(self):
        return self.text


class VoteForComment(models.Model):
    VOTE_CHOICES = (
        (1, 'Like'),
        (-1, 'Dislike'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(CommentsVideo, on_delete=models.CASCADE, related_name='votes')
    value = models.SmallIntegerField(choices=VOTE_CHOICES)

    class Meta:
        unique_together = ('user', 'comment')


class LikesComment(models.Model):
    user = models.ForeignKey(User, related_name="likeu_comment", on_delete=models.CASCADE)
    comment = models.ForeignKey(CommentsVideo, on_delete=models.CASCADE)
    count_likes = models.IntegerField(default=0)
    added_at = models.DateTimeField(auto_now_add=True, verbose_name="Data")

    def __str__(self):
        return str(self.count_likes)