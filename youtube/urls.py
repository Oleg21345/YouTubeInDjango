from django.urls import path
from youtube.views.views import *
from youtube.views.registration_view import *


urlpatterns = [
    # Class View
    path("", Home.as_view(), name="home"),
    # path("createvideo/", CreateView.as_view(), name="createvideo"),

    # Func View
    path("createvideo/", create_video, name="createvideo"),
    path("login/", user_login, name="login"),
    path("logout/", user_logout, name="logout"),
    path("register/", register, name="register"),


]









