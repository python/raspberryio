from django.conf.urls import patterns, include, url
from mezzanine.conf import settings

from django.views.decorators.cache import cache_page


ACCOUNT_URL = '/account/'
SIGNUP_URL = getattr(settings, 'SIGNUP_URL',
    '/%s/signup/' % ACCOUNT_URL.strip("/")
)

LOGIN_URL = settings.LOGIN_URL
LOGOUT_URL = settings.LOGOUT_URL

urlpatterns = patterns('raspberryio.userprofile.views',

    # custom django-activity-stream based views
    url(r'^(?P<username>[\w.\-]+)/stream/$', 'profile_actions', name='profile-actions'),
    url(r'^(?P<username>[\w.\-]+)/(?P<relation>[followers|following]+)/$', 'profile_related_list', name='profile-related'),

    # Mezzanine accounts urls (Put any custom ones above)
    url(r'^%s/$' % (LOGIN_URL.strip("/"),), cache_page(60 * 120)("login"), name="login"),
    url(r'^%s/$' % (LOGOUT_URL.strip("/"),), cache_page(60 * 120)("logout"), name="logout"),
    url(r'^%s/$' % (SIGNUP_URL.strip("/"),), cache_page(60 * 120)("signup"), name="signup"),

    url('^', include('mezzanine.accounts.urls')),
)
