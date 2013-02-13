import urlparse

from django.http import HttpResponse
from django.utils import simplejson


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
