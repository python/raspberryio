from django.conf.urls import patterns, url


urlpatterns = patterns('raspberryio.project.views',
    url(r'^$', 'project_list', name='project-list'),
    url(
        r'^view/(?P<project_slug>[\w-]+)/$',
        'project_detail', name='project-detail'
    ),
    url(r'^add/$', 'project_create_edit', name='project-create-edit'),
    url(
        r'^edit/(?P<project_slug>[\w-]+)/$',
        'project_create_edit',
        name='project-create-edit'
    ),
)
