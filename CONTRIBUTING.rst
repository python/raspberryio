Contributing to raspberryio
================================

Raspberryio is an open-source project and we welcome community
contributions.


Submit an Issue
---------------

Issues are managed on Github. If you think the bug is on the front-end, such as
a bug in JavaScript or something styling-related, then please include details
about the browser, operating system and/or device being used.

Issues are also used to track new features. If you have a feature you would
like to see then you can submit a ticket. Please add the "proposal" label to
these tickets.


Get the Source
--------------

Feel free to fork raspberryio and make your own changes. You can download the
full source by cloning the git repo::

    git clone git@github.com:caktus/raspberryio.git

Follow the instructions in the README.rst file to setup your development
environment.


Workflow
--------

Please submit a pull request to have it merged in. Here's a quick guide:

#. Fork the repo.

#. Run the tests according to the directions in the README. We only take pull
   requests with passing tests, and it's great to know that you have a clean
   slate.

#. Add a test for your change. Only refactoring and documentation changes
   require no new tests. If you are adding functionality or fixing a bug, we
   need a test.

#. Follow `PEP8 style conventions <http://www.python.org/dev/peps/pep-0008/>`_.
   Use 4 spaces instead of tabs. The project might not always follow PEP8 to
   the letter. When in doubt, follow the existing code style.

#. Push to your fork and submit a pull request to `caktus:develop`.

#. Now you're waiting on the maintainers. We'll typically review and comment on
   your pull request within 3 business days. We may suggest some changes,
   improvements, or alternatives to be used before pulling in the changeset.

#. If your change is accepted, you'll be added in the AUTHORS file.
