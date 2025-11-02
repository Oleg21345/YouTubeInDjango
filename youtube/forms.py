from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from youtube.models import Video, PlayList

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username",
                               max_length=150,
                               widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(label="Password",
                               max_length=150,
                               widget=forms.PasswordInput(attrs={"class": "form-control"}))


class RegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    username = forms.CharField(max_length=150,
                               widget=forms.TextInput(attrs={"class": "form-control",
                                                             "placeholder": "Username"}))

    email = forms.EmailField(widget=forms.TextInput(
        attrs={"class": "form-control", "placeholder": "Email"}
    ))

    password1 = forms.CharField(max_length=150,
                               widget=forms.PasswordInput(attrs={"class": "form-control",
                                                                 "placeholder": "Password"}))
    password2 = forms.CharField(max_length=150,
                               widget=forms.PasswordInput(attrs={"class": "form-control",
                                                                 "placeholder": "Password repeat"}))
class VideoCreateForm(forms.ModelForm):
    photo = forms.ImageField()
    video = forms.FileField()

    class Meta:
        model = Video
        fields = ["title", "desc", "is_published", "photo", "video"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Put title to your video"}),
            "desc": forms.Textarea(attrs={"class": "form-control", "placeholder": "Put description to your video"}),
        }


class VideoUpdateForm(forms.ModelForm):

    class Meta:
        model = Video
        fields = ["title", "desc", "is_published"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Put title to your video"}),
            "desc": forms.Textarea(attrs={"class": "form-control", "placeholder": "Put description to your video"}),
        }


class UpdateOnlyPhoto(forms.ModelForm):
    photo = forms.ImageField()

    class Meta:
        model = Video
        fields = ["photo"]

class PlayListForm(forms.ModelForm):
    access = forms.ChoiceField(
        choices=PlayList.ACCESS_CHOICES,
        label="Playlist Access",
        help_text="Public — visible to everyone, Unlisted — accessible via link, Private — only you can see",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    name = forms.CharField(
        max_length=150,
        label="Playlist Name",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text="Enter a name for your playlist"
    )

    class Meta:
        model = PlayList
        fields = ["name", "access"]

