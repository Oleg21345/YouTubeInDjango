from django import template
from youtube.models import Notificated

register = template.Library()

@register.simple_tag(takes_context=True)
def unread_count(context):
    request = context['request']
    if request.user.is_authenticated:
        return Notificated.objects.filter(user=request.user, is_read=False).count()
    return 0
