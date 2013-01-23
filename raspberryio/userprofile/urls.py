from django.conf.urls import patterns, include, url


urlpatterns = patterns('',

    # Mezzanine urls (Put any custom ones above)
    url('^', include('mezzanine.urls')),
)
