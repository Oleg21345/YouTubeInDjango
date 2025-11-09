from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.db.models import F, Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from youtube.models import Video, WatchLater, LikesVideo, PlayList, CommentsVideo, Autor, VoteForComment
from youtube.forms import VideoCreateForm, VideoUpdateForm,UpdateOnlyPhoto, PlayListForm, ComentVideoForm
from youtube.s3.s3_views import main, delete_s3_file
from youtube.s3.data_compresor import compress_photo, compresor_video_in_memory, compress_existing_videos,ffmpeg_url
from youtube.s3.validate_photo import validate_image_size
import io


def get_subscription_status(user, video):

    if not hasattr(user, "autor"):
        return None

    user_autor = user.autor

    if user_autor == video.autor:
        return "owner"

    if video.autor in user_autor.subscriptions.all():
        return "subscribed"

    return "not_subscribed"


class Home(ListView):
    model = Video
    context_object_name = "videos"
    template_name = "movies/index.html"
    extra_context = {"title": "YouTube"}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        video = Video.objects.filter(is_published=True)
        autor = Autor.objects.get(user=self.request.user)
        context["autor"] = autor
        context["videos"] = video
        return context

class VideoDetail(DetailView):
    model = Video
    context_object_name = "video"
    template_name = "movies/video_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.object.title
        video = self.object
        user = self.request.user

        slug = self.kwargs["slug"]
        Video.objects.filter(slug=slug).update(watch=F("watch") + 1)

        context["like_count"] = video.votes.filter(value=1).count()
        context["dislike_count"] = video.votes.filter(value=-1).count()

        context["user_comment_votes"] = {}
        if user.is_authenticated:
            votes = VoteForComment.objects.filter(user=user, comment__video=video)
            context["user_comment_votes"] = {vote.comment.id: vote.value for vote in votes}

            vote = video.votes.filter(user=user).first()
            context["user_vote"] = vote.value if vote else None
        else:
            context["user_vote"] = None

        context["form_comm"] = ComentVideoForm()
        context["subscription_status"] = get_subscription_status(user, video)

        return context

class EditText(UpdateView):
    model = Video
    template_name = "movies/update_video.html"
    form_class = VideoUpdateForm

    def get_success_url(self):
        return reverse("video_detail", kwargs={"slug": self.object.slug})

class EditPhoto(UpdateView):
    model = Video
    template_name = "movies/update_onlyvideo.html"
    form_class = UpdateOnlyPhoto

    def form_valid(self, form):
        video = self.get_object()
        old_photo_url = video.url_photo
        photo_file = self.request.FILES.get("photo")
        if not photo_file:
            messages.error(self.request, "No photo uploaded!")
            return redirect("createvideo")
        try:
            validate_image_size(photo_file)
            photo_buffer = compress_photo(photo_file)
        except ValueError as e:
            messages.error(self.request, str(e))
            return redirect("createvideo")
        photo_buffer.seek(0)
        new_photo_url  = main(photo_buffer)

        if old_photo_url and old_photo_url != new_photo_url:
            delete_s3_file(old_photo_url)
        video.url_photo = new_photo_url
        video.save()

        messages.success(self.request, "Photo successfully updated!")
        return redirect("video_detail", slug=video.slug)

class WatchLaterList(ListView):
    model = WatchLater
    context_object_name = "videos"
    template_name = "movies/watch_later.html"

class LikeVideoList(ListView):
    model = LikesVideo
    context_object_name = "videos"
    template_name = "movies/likes_video.html"

class CommentUpdate(UpdateView):
    model = CommentsVideo
    form_class = ComentVideoForm
    template_name = "movies/video_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["video"] = self.object.video
        return context

    def get_success_url(self):
        return reverse_lazy("video_detail", kwargs={"slug": self.object.video.slug})

class CommentDelete(DeleteView):
    model = CommentsVideo
    success_url = reverse_lazy("post_detail")
    context_object_name = "comment"
    template_name = "movies/comment_confirm_delete.html"
    extra_context = {"title": "Delete comment"}

    def get_success_url(self):
        next_url = self.request.GET.get("next")
        if next_url:
            return next_url
        return reverse_lazy("video_detail", kwargs={"slug": self.object.video.slug})

class SearchResults(ListView):
    model = Video
    template_name = "movies/search_results.html"
    context_object_name = "videos"

    def get_queryset(self):
        word = self.request.GET.get("q")
        if word:
            return Video.objects.filter(
                Q(title__icontains=word) | Q(desc__icontains=word)
            )
        return Video.objects.none()

def create_video(request):
    if request.method == "POST":
        form = VideoCreateForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.autor = request.user

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


@login_required
def toggle_watch_later(request, video_slug):
    video = get_object_or_404(Video, slug=video_slug)
    existing_entry = WatchLater.objects.filter(user=request.user, video=video)

    if existing_entry.exists():
        existing_entry.delete()
        message = "Removed from Watch Later"
    else:
        WatchLater.objects.create(user=request.user, video=video)
        message = "Added to Watch Later"

    messages.info(request, message)
    return redirect(request.META.get("HTTP_REFERER", "home"))


def share_link(request, video_slug):
    video_url = request.build_absolute_uri(f"/video/{video_slug}/")
    context = {
        "video_url": video_url,
    }
    return render(request,"movies/index.html", context)
from django.http import JsonResponse

def add_play_list(request, video_slug):
    video = get_object_or_404(Video, slug=video_slug)

    if request.method == "POST":
        form = PlayListForm(request.POST)
        if form.is_valid():
            playlist = form.save(commit=False)
            playlist.user = request.user
            playlist.save()
            playlist.videos.add(video)

            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                return JsonResponse({"success": True, "message": "Playlist created successfully!"})

            return redirect("home")
        else:
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                html = render(request, "movies/add_playlist_modal.html", {"form": form, "video": video}).content.decode("utf-8")
                return JsonResponse({"success": False, "form_html": html})
    else:
        form = PlayListForm()

    return render(request, "movies/add_playlist_modal.html", {"form": form, "video": video})

def delete_from_play_list(request, play_list_slug, video_slug):
    playlist = get_object_or_404(PlayList, slug=play_list_slug)
    video = get_object_or_404(Video, slug=video_slug)

    playlist.videos.remove(video)
    messages.success(request, f"Video '{video.title}' removed from playlist {playlist.name}")

    return redirect("home")

def add_from_play_list(request, play_list_slug, video_slug):
    playlist = get_object_or_404(PlayList, slug=play_list_slug)
    video = get_object_or_404(Video, slug=video_slug)

    playlist.videos.add(video)
    messages.success(request, f"Video '{video.title}' removed from playlist {playlist.name}")

    return redirect("home")


def add_comment(request, slug, parent_slug=None):
    video = get_object_or_404(Video, slug=slug)
    top_comments = video.commentsvideo_set.filter(reply_to_comment__isnull=True)

    if request.method == "POST":
        form = ComentVideoForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.video = video

            parent_slug_post = form.cleaned_data.get("reply_to_slug")
            if parent_slug_post:
                parent_comment = get_object_or_404(CommentsVideo, slug=parent_slug_post)
                comment.reply_to_comment = parent_comment

            comment.save()
            messages.success(request, "Comment added successfully!")
            return redirect("video_detail", slug=video.slug)
    else:
        form = ComentVideoForm(initial={"reply_to_slug": parent_slug})

    context = {
        "video": video,
        "form_comm": form,
        "parent_slug": parent_slug
    }

    return render(request, "movies/video_detail.html", context)


