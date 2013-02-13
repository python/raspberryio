from django.contrib.auth.models import User
from django import template

from actstream.models import Follow

register = template.Library()

@register.filter
def followers(username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise template.TemplateSyntaxError("%r is not a valid username" % username)
    return len(Follow.objects.followers(user))

@register.filter
def following(username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise template.TemplateSyntaxError("%r is not a valid username" % username)
    return len(Follow.objects.following(user))
