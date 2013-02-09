from django.conf.urls import patterns, include, url

urlpatterns = patterns('raspberryio.userprofile.views',
    url(r'^(?P<username>[\w.\-]+)/(?P<relation>[followers|following]+)/$', 'profile_related_list', name='profile-related'),

    # Mezzanine accounts urls (Put any custom ones above)
    url('^', include('mezzanine.accounts.urls')),
)
