from django.conf.urls import patterns, url


urlpatterns = patterns('raspberryio.project.views',
    # Project list
    url(r'^$', 'project_list', name='project-list'),
    # Project detail
    url(
        r'^view/(?P<project_slug>[\w-]+)/$',
        'project_detail', name='project-detail'
    ),
    # Create project
    url(r'^add/$', 'project_create_edit', name='project-create-edit'),
    # Edit project
    url(
        r'^edit/(?P<project_slug>[\w-]+)/$', 'project_create_edit',
        name='project-create-edit'
    ),
    # Create project step
    url(
        r'^add-step/(?P<project_slug>[\w-]+)/$', 'project_step_create_edit',
        name='project-step-create-edit'
    ),
    # Edit project step
    url(
        r'^edit-step/(?P<project_slug>[\w-]+)/(?P<project_step_number>[\d]+)/$',
        'project_step_create_edit',
        name='project-step-create-edit'
    ),

    # Delete project
    url(
        r'^delete/(?P<project_pk>[\d]+)/$', 'project_delete',
        name='project-delete'
    ),
    # Delete project step
    url(
        r'^delete-step/(?P<project_step_pk>[\d]+)/$', 'project_step_delete',
        name='project-step-delete'
    ),

    # --- Ajax views

    # Publish a project
    url(
        r'^publish/(?P<project_slug>[\w-]+)/$', 'publish_project',
        name='publish-project'
    ),

    # Upload, download, or delete Gallery Images
    url(
        r'^add-image/' + \
        '(?:(?P<project_slug>[\w-]+)/)?/(?:(?P<project_step_number>[\d]+)/)?$',
        'gallery_image_create', name='gallery-image-upload',
    ),
    url(
        r'^image/(?P<project_slug>[\w-]+)/(?P<project_step_number>[\d]+)/$',
        'gallery_image_download', name='gallery-image-download',
    ),
    url(
        r'^delete-image/(?P<project_image_id>\d+)/$',
        'gallery_image_delete', name='gallery-image-delete',
    ),
)
