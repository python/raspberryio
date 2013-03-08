from functools import wraps
from collections import Counter
from datetime import timedelta
from operator import itemgetter
import urlparse

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.utils import simplejson
from django.views.decorators.cache import cache_page

from actstream.models import Action
from mezzanine.utils.timezone import now


YOUTUBE_SHORT_URL = "youtu.be"

YOUTUBE_DOMAINS = ("www.youtube.com",
                   "youtube.com",
                   "m.youtube.com",
                   YOUTUBE_SHORT_URL
                   )


def get_youtube_video_id(url):
    "Consumes a URL and extracts the video id"
    video_id = ''
    data = urlparse.urlparse(url)
    if data.netloc.lower() in YOUTUBE_DOMAINS:
        if data.netloc.lower() != YOUTUBE_SHORT_URL:
            query = urlparse.parse_qs(data.query)
            video_id = query.get('v', '')[0]
        else:
            video_id = data.path.split('/')[1]
    return video_id


class AjaxResponse(HttpResponse):
    """Like hilbert.JsonResponse but uses text/plain for junky browsers"""

    def __init__(self, request, obj='', *args, **kwargs):
        content = simplejson.dumps(obj, {})
        http_accept = request.META.get('HTTP_ACCEPT', 'application/json')
        mimetype = 'application/json' \
            if 'application/json' in http_accept else 'text/plain'
        super(AjaxResponse, self).__init__(content, mimetype, *args, **kwargs)
        self['Content-Disposition'] = 'inline; filename=files.json'


def get_active_users(days=7, number=4):
    """
    Return a queryset of the most active users for the given `days` and limited
    to `number` users. Defaults to 7 days and 4 users.
    """
    week_ago = now() - timedelta(days=days)
    actions = Action.objects.model_actions(User) \
        .filter(timestamp__gte=week_ago) \
        .values_list('actor_object_id', flat=True)
    most_active_user_pks = map(
        itemgetter(0), Counter(actions).most_common(number * 2)
    )
    return User.objects.filter(
        pk__in=most_active_user_pks, is_active=True, profile__isnull=False
    )[:number]


def cache_on_auth(timeout):
    def decorated(view_func):
        @wraps(view_func)
        def _(request, *args, **kwargs):
            # Anonymous might be a better user_key, but is a valid username
            user_key = '~~~~' if not request.user.is_authenticated \
                else request.user.username
            return cache_page(
                timeout, key_prefix="user:%s" % user_key
            )(view_func)(request, *args, **kwargs)
        return _
    return decorated
