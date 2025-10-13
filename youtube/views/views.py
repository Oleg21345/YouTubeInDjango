from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.contrib import messages
from youtube.models import Video
from youtube.forms import VideoCreateForm
from youtube.s3.s3_views import main
from youtube.s3.data_compresor import compress_photo

class Home(ListView):
    model = Video
    context_object_name = "videos"
    template_name = "movies/index.html"
    extra_context = {"title": "YouTube"}


def create_video(request):
    if request.method == "POST":
        form = VideoCreateForm(request.POST, request.FILES)
        if form.is_valid():

            video = form.save(commit=False)
            video.autor = request.user.autor

            photo = request.FILES.get("photo")
            try:
                photo_buffer = compress_photo(photo)
            except ValueError as e:
                messages.error(request, str(e))
                return redirect("create_video")
            video_url = request.FILES.get("video")

            video.url_photo = main(photo_buffer)
            video.url_video = main(video_url)
            video.save()
            return redirect("home")
    else:
        form = VideoCreateForm()

    context = {
        "title": "Post Video",
        "form": form,
    }
    return render(request, "movies/createvideo.html", context)













