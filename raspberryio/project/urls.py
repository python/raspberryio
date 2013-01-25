from django.conf.urls import patterns, url


urlpatterns = patterns('raspberryio.project.views',
    url(r'^$', 'project_list', name='project-list'),
    url(
        r'^(?P<project_slug>[\w-]+)/$',
        'project_detail', name='project-detail'
    ),
)
