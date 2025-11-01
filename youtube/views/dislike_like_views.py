from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from youtube.models import Video, Vote, LikesVideo
from youtube.notification_system import add_notification

def like_video(request, slug):
    video = get_object_or_404(Video, slug=slug)
    vote, created = Vote.objects.get_or_create(user=request.user,
                                               video=video)
    if vote.value == 1:
        vote.delete()
        vote.save()
    else:
        vote.value = 1
        vote.save()

    return redirect("video_detail", slug=slug)



def dislike_video(request, slug):
    video = get_object_or_404(Video, slug=slug)
    vote, created = Vote.objects.get_or_create(user=request.user,
                                               video=video)
    if vote.value == -1:
        vote.delete()
        vote.save()
    else:
        vote.value = -1
        vote.save()

    return redirect("video_detail", slug=slug)


def post_vote(request, slug, value):
    video = get_object_or_404(Video, slug=slug)
    user = request.user

    if value not in["1", "-1"]:
        return redirect("video_detail", slug=slug)

    value = int(value)
    try:
        vote = Vote.objects.get(user=user, video=video)

        if vote.value == value:
            vote.delete()
        else:
            vote.value = value
            vote.save()
    except Vote.DoesNotExist:
        Vote.objects.create(user=user, video=video, value=value)

    if value == 1:
        existing_entry = LikesVideo.objects.filter(user=request.user, video=video)
        if existing_entry.exists():
            existing_entry.delete()
        else:
            LikesVideo.objects.create(user=request.user, video=video)

    if video.autor != user:
        action = "лайкнув" if value == 1 else "дизлайкнув"
        add_notification(
            user=video.autor,
            from_user=user,
            message=f"{action} ваш пост.",
            not_count=1
        )

    return redirect("video_detail", slug=slug)

