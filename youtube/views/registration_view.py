from django.contrib.auth import login, logout
from django.shortcuts import redirect, render
from django.contrib import messages
from youtube.forms import LoginForm, RegistrationForm
from youtube.models import Autor
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


def user_login(request):
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Success Login!")
            return redirect("home")
    else:
        form = LoginForm()

    context = {"title": "Login", "form": form}
    return render(request, "movies/registration/login.html", context)

def user_logout(request):
    logout(request)
    messages.success(request, "Success Logout!")
    return redirect("home")


def register(request):
    if request.method == "POST":
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Success Registration!")
            return redirect("login")
    else:
        form = RegistrationForm()

    context = {
        "title": "Registration",
        "form": form,
    }
    return render(request, "movies/registration/register.html", context)



@receiver(post_save, sender=User)
def create_autor(sender, instance, created, **kwargs):
    if created:
        Autor.objects.create(user=instance, nickname=instance.username, pseudonym=f"@{instance.username}")










