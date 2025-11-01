from django.shortcuts import render


def notificated_view(request):
    unread_before = list(request.user.user_notif.filter(is_read=False).values_list('id', flat=True))

    request.user.user_notif.filter(is_read=False).update(is_read=True)
    notifications = request.user.user_notif.order_by("-create_at")
    context = {
        'notifications': notifications,
        'newly_read_ids': unread_before,
    }
    return render(request, "movies/notification.html", context)







