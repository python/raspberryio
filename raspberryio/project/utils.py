from django.http import HttpResponse
from django.utils import simplejson


class AjaxResponse(HttpResponse):
    """Like hilbert.JsonResponse but uses text/plain for junky browsers"""

    def __init__(self, request, obj='', *args, **kwargs):
        content = simplejson.dumps(obj, {})
        http_accept = request.META.get('HTTP_ACCEPT', 'application/json')
        mimetype = 'application/json' \
            if 'application/json' in http_accept else 'text/plain'
        super(AjaxResponse, self).__init__(content, mimetype, *args, **kwargs)
        self['Content-Disposition'] = 'inline; filename=files.json'
