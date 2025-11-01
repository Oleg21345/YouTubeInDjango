from django.urls import path
from youtube.views.views import *
from youtube.views.registration_view import *
from youtube.s3.decode_file import stream_video
from youtube.views.dislike_like_views import like_video, dislike_video, post_vote
from youtube.views.notificate_views import notificated_view

urlpatterns = [
    # Class View
    path("", Home.as_view(), name="home"),
    path("video/<slug:slug>/", VideoDetail.as_view(), name="video_detail"),
    path("profile/<slug:slug>/", Profile.as_view(), name="profile"),
    path("profile_settings/<slug:slug>/", ProfileSettings.as_view(), name="profile_settings"),
    path("watch_later_list/<slug:slug>/", WatchLaterList.as_view(), name="watch_later_list"),
    path("liked_video_list/<slug:slug>/", LikeVideoList.as_view(), name="likes_list"),
    path("update/<slug:slug>/", EditText.as_view(), name="edit_video"),
    path("update/<slug:slug>/photo/", EditPhoto.as_view(), name="edit_only_photo"),

    # path("createvideo/", CreateView.as_view(), name="createvideo"),

    # Func View
    path("createvideo/", create_video, name="createvideo"),
    path("login/", user_login, name="login"),
    path("logout/", user_logout, name="logout"),
    path("register/", register, name="register"),
    path("stream/<slug:video_slug>/", stream_video, name="stream_video"),
    path('video/<slug:slug>/like/', like_video, name='like_video'),
    path('video/<slug:slug>/dislike/', dislike_video, name='dislike_video'),
    path('video/<slug:slug>/vote/<str:value>/', post_vote, name='video_vote'),
    path('notificated/', notificated_view, name='notificated'),
    path('watch_later/<slug:video_slug>/', toggle_watch_later, name="watch_later"),
    path('share_video/<slug:video_slug>/', share_link, name="share_link"),


]









