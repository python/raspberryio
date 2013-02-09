from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin

from mezzanine.core.views import direct_to_template

admin.autodiscover()


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    # Static homepage template for now
    url(r"^$", direct_to_template, {"template": "homepage.html"}, name="home"),

    # RaspberryIO apps
    url(r'^projects/', include('raspberryio.project.urls')),
    url(r'^accounts/', include('raspberryio.userprofile.urls')),

    # django-activity-streams
    url('^activity/', include('actstream.urls')),

    # Mezzanine urls
    url(r'^', include('mezzanine.urls')),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Adds ``STATIC_URL`` to the context of error pages, so that error
# pages can use JS, CSS and images.
handler404 = "mezzanine.core.views.page_not_found"
handler500 = "mezzanine.core.views.server_error"
