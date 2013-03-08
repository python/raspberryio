from django.conf.urls import patterns, include, url


urlpatterns = patterns('raspberryio.userprofile.views',
    # custom django-activity-stream based views
    url(r'^(?P<username>[\w.\-]+)/stream/$', 'profile_actions', name='profile-actions'),
    url(r'^(?P<username>[\w.\-]+)/(?P<relation>[followers|following]+)/$', 'profile_related_list', name='profile-related'),

    # Override just the login view
    url(r'^login/$', 'login', name='login'),
    url('^', include('mezzanine.accounts.urls')),
)
