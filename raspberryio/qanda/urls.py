from django.conf.urls import patterns, url


urlpatterns = patterns('raspberryio.qanda.views',
    url(r'^$', 'question_list', name='question-list'),
    url(r'^view/(?P<question_slug>[\w-]+)/$',
        'question_detail',
        name='question'),
    url(r'^ask/$',
        'question_create_edit',
        name='question-create-edit'),
    url(r'^edit/(?P<question_slug>[\w-]+)/$',
        'question_create_edit',
        name='question-create-edit'),
)
