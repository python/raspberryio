.. _getcode:

Get the code
============

Here's how you can get the `Raspberry IO`_ site running on your computer.

Install Dependencies
--------------------

Raspberry IO is a Django project built on top of the `Mezzanine CMS`_,
using PostgreSQL as our database. To get started, you will need the
following programs installed. These should be installed using your
operating system's standard package management system:

- Python >= 2.6 (2.7 recommended)
- `pip >= 1.1 <http://www.pip-installer.org/>`_
- `virtualenv >= 1.7 <http://www.virtualenv.org/>`_
- `virtualenvwrapper >= 3.0 <http://pypi.python.org/pypi/virtualenvwrapper>`_
- PostgreSQL >= 8.4 (9.1 recommended)
- git >= 1.7

Clone the repository
--------------------

Clone the `Raspberry IO repository`_ from Github:

.. code-block:: console

    $ git clone git@github.com:caktus/raspberryio.git
    Cloning into 'raspberryio'...
    remote: Counting objects: 3860, done.
    remote: Compressing objects: 100% (1749/1749), done.
    remote: Total 3860 (delta 2081), reused 3845 (delta 2069)
    Receiving objects: 100% (3860/3860), 2.98 MiB | 861.00 KiB/s, done.
    Resolving deltas: 100% (2081/2081), done.

You'll now have a new ``raspberryio`` subdirectory containing the code.

Set up your environment
-----------------------

Change into the ``raspberryio`` directory:

.. code-block:: console

    $ cd raspberryio
    $


Create a virtual environment to work in and activate it:

.. code-block:: console

    $ mkvirtualenv --distribute raspberryio
    ...
    $ pip install -r requirements/dev.txt
    ...
    $


Create a local settings file and set your ``DJANGO_SETTINGS_MODULE``
to use it:

.. code-block:: console

    $ cp raspberryio/settings/local.example.py raspberryio/settings/local.py
    $ echo "export DJANGO_SETTINGS_MODULE=raspberryio.settings.local" >> $VIRTUAL_ENV/bin/postactivate
    $ echo "unset DJANGO_SETTINGS_MODULE" >> $VIRTUAL_ENV/bin/postdeactivate
    $


Add the project directory to the virtualenv, deactivate and reactivate
it to set up the environment variables above:

.. code-block:: console

    $ add2virtualenv .
    $ deactivate
    $ workon raspberryio
    $

Set up the database
-------------------

Create the Postgres database.

.. code-block:: console

    $ createdb -E UTF-8 raspberryio


Run the initial syncdb/migrate. When asked to create a superuser,
answer ``no``.

.. code-block:: console

    $ django-admin.py syncdb
    $ django-admin.py migrate

.. Warning::
   Creating a superuser in the syncdb step will trigger the error
   ``django.db.utils.DatabaseError: relation "userprofile_profile"
   does not exist`` because of a required one-to-one relation with a
   user profile model that doesn't exist in the database yet.

**Now**, create a superuser (This will also create the profile correctly):

.. code-block:: console

    $ django-admin.py createsuperuser


Master versus Develop branch
----------------------------

The ``master`` branch in the Raspberry IO repository represents the
code that is running on the production site, raspberry.io. All
development should happen on the ``develop`` branch. Once things are
shown to be stable, they will be migrated to the ``master`` branch by
the project maintainers.

.. code-block:: console

    $ git checkout develop
    Branch develop set up to track remote branch develop from origin.
    Switched to a new branch 'develop'
    $

Run the tests and server
------------------------

Verify that everything is okay by running Raspberry IO's tests.

.. code-block:: console

    $ django-admin.py test
    [lots of output omitted]
    Ran 158 tests in 62.170s

    OK
    [lots of output omitted]
    $

Then run the development server and play around!

.. code-block:: console

    $ django-admin.py runserver

.. _Raspberry IO: http://raspberry.io/
.. _Mezzanine CMS: http://mezzanine.jupo.org/
.. _Raspberry IO repository: https://github.com/caktus/raspberryio
