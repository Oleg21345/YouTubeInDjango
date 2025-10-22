from tkinter.constants import CASCADE
from django.contrib.auth.models import User
from django.db import models
import uuid
# Create your models here.



class Autor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="autor")
    slug = models.SlugField(default=str(uuid.uuid4())[:8])
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
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE, related_name="video")
    is_published = models.BooleanField(default=False)
    watch = models.IntegerField(default=0)
    like = models.IntegerField(default=0)
    dislike = models.IntegerField(default=0)
    url_photo = models.URLField(max_length=500)
    url_video = models.URLField()
    url_video_240 = models.URLField(blank=True, null=True)
    url_video_360 = models.URLField(blank=True, null=True)
    url_video_720 = models.URLField(blank=True, null=True)
    url_video_1080 = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title



