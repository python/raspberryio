.. _developer:

Developer Documentation
=======================

Raspberry IO is a site to help users share knowledge about using the
Python language on the Raspberry Pi platform. If you've gotten to this
page, then you are interested in helping with the development of the
site. Thanks! First, please check out the :doc:`contribution docs
<index>`, which explains how to get the code running and how to make
sure your contributions meet our standards.

This document will give a high level overview of the site and its
components. There are 4 main areas to the site, which are linked in
the footer of the site:

`Create <http://raspberry.io/projects/add/>`_
    This is where you share information about Raspberry Pi projects
    you create.
`Explore <http://raspberry.io/projects/>`_
    This is where you can browse projects that community members have
    created.
`Learn <http://raspberry.io/wiki/>`_
    This is a wiki where you can learn about the Raspberry Pi and
    contribute your own knowledge to the community.
`Community <http://raspberry.io/community/>`_
    This includes a RSS aggregator which collects interesting
    Raspberry Pi posts and a Q&A forum where you can ask questions and
    help other users.

In addition, the site features `social
<http://raspberry.io/dashboard/>`_ features where you can see
information about other users, follow them, and view how they are
interacting with the site.

Detailed info
-------------

The 'Create' and 'Explore' sections are built with the
``raspberryio.project`` app. It allows users to create projects with
arbitrary numbers of steps (think steps in a tutorial), images, video
links, etc. Projects can be labeled as 'Featured' by site admins.
Projects can be in draft or published state.

The 'Learn' section is a wiki. We use a `fork of django-wiki
<https://github.com/daaray/django-wiki>`_. The main reason for the
fork is to use the Pillow imaging library rather than PIL, as Pillow
installation has been simpler in our experience. We also heavily
modified the templates.

As mentioned above, the 'Community' section includes two pieces of
functionality. The Feed aggregator is in ``raspberryio.aggregator``.
This app allows users to submit RSS feeds and admins to approve or
deny them. Feeds are then displayed to the community. The `django-push
<https://django-push.readthedocs.org/en/latest/>`_ app is used to
manage the PubSub process.

The second portion is a Q&A forum which is included in the app
``raspberryio.qanda``. This datamodel includes questions and answers,
and allows users to upvote good answers. This is again built on top of
Mezzanine models.

The social aspect is built by various packages. The
``raspberryio.userprofile`` app collects information about users. The
`django-activity-stream
<https://django-activity-stream.readthedocs.org/en/latest/>`_ app is
used to allow people to follow the activity of other users.


Search:
-------

Search is implemented through the Mezzanine search facilities. We
specify which models and fields we are interested in indexing in the
``SEARCH_MODEL_INDEXES`` dictionary in the base.py settings file.
Proxy models which subclass Searchable are dynamically created in the
``raspberryio.search`` app, containing only those fields with the
desired weights. (Fields with higher weights will be shown to the user
before those with lower weights).

Searching the wiki is a special case. Since each revision of the wiki
is saved, we could get multiple revisions of the same article show up
in search results. So, instead of feeding the wiki.ArticleRevision
model to Mezzanine, we have created an app
``raspberryio.search_models`` which extracts only the latest revision
of each article and indexes that. The ``search_models`` app maintains
this flattened representation of the latest revision in its own table,
and should be used in the future for any other models with a similar
structure. Using something in MPTT or similar might be better than the
current "flatten and copy" behavior, but this is what we have for now.

Comments:
---------

We use `Disqus <http://disqus.com/>`_ to allow users to comment on
individual projects. The ``DISQUS_HOSTNAME`` (in Django settings) is
set to ``http://raspberry.io` so that non-production sites can see the
commenting functionality. ``DISQUS_SHORTNAME`` is set to
``raspberryio`` for production and ``raspberryio-staging`` for the
staging site. If local developers wish to test commenting for some
reason, then they should create a DISQUS account, set up a new
shortname and use that for ``DISQUS_SHORTNAME`` in
``raspberryio.settings.base``.
