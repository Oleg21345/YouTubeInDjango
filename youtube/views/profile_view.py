from django.views.generic import DetailView
from youtube.models import Video, Autor


class Profile(DetailView):
    model = Autor
    context_object_name = "autor"
    template_name = "movies/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs["slug"]
        print(f"DEBUG slug {slug}")
        video = Video.objects.filter(autor__autor__slug=slug)
        print(f"DEBUG video {video}")
        context["videos"] = video
        context["videos_count"] = context["videos"].count()

        return context

class ProfileSettings(DetailView):
    model = Autor
    context_object_name = "autor_settings"
    template_name = "movies/profile_settings.html"