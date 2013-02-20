from django.conf.urls import patterns, url


urlpatterns = patterns('raspberryio.qanda.views',
    url(r'^$', 'index', name='community-index'),
    url(r'^ask/$', 'question_list', name='question-list'),
    url(r'^view/(?P<question_slug>[\w-]+)/$',
        'question_detail',
        name='question'),
    # Create/edit questions
    url(r'^question/$',
        'question_create_edit',
        name='question-create-edit'),
    url(r'^edit-question/(?P<question_slug>[\w-]+)/$',
        'question_create_edit',
        name='question-create-edit'),
    # Create/edit answers
    url(r'^answer/(?P<question_slug>[\w-]+)/$',
        'answer_create_edit',
        name='answer-create-edit'),
    url(r'^edit-answer/(?P<question_slug>[\w-]+)/(?P<answer_pk>[\w-]+)/$',
        'answer_create_edit',
        name='answer-create-edit'),
    # Upvote answer Ajax view
    url(r'^upvote/(?P<answer_pk>[\d]+)/$',
        'upvote_answer',
        name='upvote-answer'
    ),
)
