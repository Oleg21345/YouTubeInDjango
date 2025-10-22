from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.contrib import messages
from youtube.models import Video
from youtube.forms import VideoCreateForm
from youtube.s3.s3_views import main
from youtube.s3.data_compresor import compress_photo, compresor_video_in_memory, compress_existing_videos,ffmpeg_url
from youtube.s3.validate_photo import validate_image_size
import io

class Home(ListView):
    model = Video
    context_object_name = "videos"
    template_name = "movies/index.html"
    extra_context = {"title": "YouTube"}


class VideoDetail(DetailView):
    model = Video
    context_object_name = "video"
    template_name = "movies/video_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.object.title

        return context


def create_video(request):
    if request.method == "POST":
        form = VideoCreateForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.autor = request.user.autor

            photo_file = request.FILES.get("photo")
            if not photo_file:
                messages.error(request, "No photo uploaded!")
                return redirect("createvideo")
            try:
                validate_image_size(photo_file)
                photo_buffer = compress_photo(photo_file)
            except ValueError as e:
                messages.error(request, str(e))
                return redirect("createvideo")
            photo_buffer.seek(0)
            video.url_photo = main(photo_buffer)

            video_file = request.FILES.get("video")
            if not video_file:
                messages.error(request, "No video uploaded!")
                return redirect("createvideo")

            video_buffer = io.BytesIO(video_file.read())
            video_buffer.seek(0)

            compressed_videos = compresor_video_in_memory(video_buffer)
            final_videos = compress_existing_videos(compressed_videos, ffmpeg_url)

            video_versions = {}

            for label, buffer in final_videos.items():
                buffer.seek(0)
                video_url = main(buffer)

                video.url_video = video_url

                # setattr(video, f"url_video_{label.replace('p','')}", video_url)
                print(f"DEBUG buffer = {buffer}")
                print(f"DEBUG Label = {label}")
                if label.endswith("_240p"):
                    video.url_video_240 = video_url
                elif label.endswith("_360p"):
                    video.url_video_360 = video_url
                elif label.endswith("_480p"):
                    video.url_video_480 = video_url
                elif label.endswith("_720p"):
                    video.url_video_720 = video_url
                elif label.endswith("_1080p"):
                    video.url_video_1080 = video_url

                video_versions[label] = video_url

            video.save()
            return redirect("home")
    else:
        form = VideoCreateForm()

    context = {
        "title": "Post Video",
        "form": form,
    }
    return render(request, "movies/createvideo.html", context)










