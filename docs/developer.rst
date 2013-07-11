.. _developer:

Developer Documentation
=======================

This is just a draft.

Raspberry IO is a site to help users share knowledge about using the
Python language on the Raspberry Pi platform. If you've gotten to this
page, then you are interested in helping with the development of the
site. Thanks! First, please check out the contribution docs, which
explain how to get the code running and how to make sure your
contributions meet our standards.

This document will give a high level overview of the site and its
components.

There are 5 main areas to the site:

Create:
-------

This is where you share information about Raspberry Pi projects you
create.

Explore:
--------

This is where you can browse projects that community members have
created.

Learn:
------

This is a wiki where you can learn about the Raspberry Pi and
contribute your own knowledge to the community.

Community:
----------

This has 2 features: 1) An RSS aggregator which collects interesting
posts about the Raspberry Pi in one place. 2) a Q&A forum where you
can ask questions and help other users

Social:
-------

You can see information about other users, follow them, and view how
they are interacting with the site.

Detailed info
-------------

The 'Create' and 'Explore' sections are built with the
raspberryio.project app, which is built on top of the Mezzanine CMS.
It allows users to create a project with an arbitrary number of steps
(think steps in a tutorial), images, video links, etc. Projects can be
labelled as 'Featured' by site admins. Projects can be in draft or
published state.

The 'Learn' section is a wiki. We use a fork of django-wiki. FIXME:
explain reason for fork.

As mentioned above, the 'Community' section includes two pieces of
functionality. The Feed aggregator is in 'raspberryio.aggregator'.
This app allows users to submit RSS feeds and admins to approve or
deny them. Feeds are then displayed to the community. django-push
is used to manage the PubSub process

The second portion is a Q&A forum which is included in the app
'raspberryio.qanda'. This datamodel includes Questions and Answers,
and allows users to upvote good Answers. This is again built on top
of Mezzanine models.

The social aspect is built by various packages. The
raspberryio.userprofile app collects information about users. The
django-activity-stream
https://django-activity-stream.readthedocs.org/en/latest/ app is used
to allow people to follow other users.


Search:
-------

FIXME: Document how search works

Design:
-------

django-bootstrap-toolkit is used as a base, but heavily modified
