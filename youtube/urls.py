from django.urls import path
from youtube.views.views import *
from youtube.views.registration_view import *
from youtube.s3.decode_file import stream_video

urlpatterns = [
    # Class View
    path("", Home.as_view(), name="home"),
    path("video/<slug:slug>/", VideoDetail.as_view(), name="video_detail"),
    # path("createvideo/", CreateView.as_view(), name="createvideo"),

    # Func View
    path("createvideo/", create_video, name="createvideo"),
    path("login/", user_login, name="login"),
    path("logout/", user_logout, name="logout"),
    path("register/", register, name="register"),
    path("stream/<slug:video_slug>/", stream_video, name="stream_video"),

]









