from django.views.generic import  DetailView
from django.contrib.auth.models import User
from youtube.models import Autor
from django.shortcuts import redirect, get_object_or_404
from youtube.models import Video
from youtube.notification_system import add_notification



def add_subscribers(request, autor_pk):
    user_follow = get_object_or_404(User, pk=autor_pk)
    autor_follow = get_object_or_404(Autor, user=user_follow)

    current_autor = get_object_or_404(Autor, user=request.user)

    autor_follow.subscribers.add(request.user)
    current_autor.subscriptions.add(user_follow)
    video = get_object_or_404(Video, pk=autor_pk)
    user = request.user
    action = "You have a new subscriber"
    add_notification(
        user=user_follow,
        from_user=request.user,
        message=action,
        not_count=1
    )
    return redirect(request.META.get("HTTP_REFERER", "/"))

def remove_subscribers(request, autor_pk):
    user_follow = get_object_or_404(User, pk=autor_pk)
    autor_follow = get_object_or_404(Autor, user=user_follow)

    current_autor = get_object_or_404(Autor, user=request.user)

    autor_follow.subscribers.remove(request.user)

    current_autor.subscriptions.remove(user_follow)

    return redirect(request.META.get("HTTP_REFERER", "/"))

class Subs(DetailView):
    model = Autor
    template_name = "movies/subs.html"
    context_object_name = "autor"





