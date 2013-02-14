from django.conf.urls import patterns, include, url

urlpatterns = patterns('raspberryio.search.views',

    # Mezzanine search urls (Put any custom ones above)
    url('^', 'search', name='search'),
)
