

Raspberry IO
========================

This is the source code for the `Raspberry IO <http://raspberry.io/>`_
site. Raspberry IO is a place to share knowledge about using the
Python programming language to control Raspberry Pi computers.

This is an open source project. We welcome contributions. You can help
by fixing bugs, planning new features, writing documentation, writing
tests, or even managing the project. Ready to contribute? Read our
`Getting Started <https://raspberry-io.readthedocs.org/>`_ document.

Travis CI Build Status
----------------------

.. image:: https://travis-ci.org/python/raspberryio.png
   :target: https://travis-ci.org/python/raspberryio

Submit an issue
------------------------

Found an issue? Have a question? We appreciate any and all feedback!
Issues are managed on `Github
<https://github.com/python/raspberryio/issues>`_. Please include
details about the browser, operating system, and/or device being used.

If you have a feature you'd like us to consider adding, please add the
"Proposal" label to your issue.

Dependencies
------------------------

Raspberry IO is a Django project using Postgres as our database. To
get started, you will need the following programs installed. These
should be installed using your operating system's standard package
management system:

- Python >= 2.6 (2.7 recommended)
- `pip >= 1.1 <http://www.pip-installer.org/>`_
- `virtualenv >= 1.7 <http://www.virtualenv.org/>`_
- `virtualenvwrapper >= 3.0 <http://pypi.python.org/pypi/virtualenvwrapper>`_
- Postgres >= 8.4 (9.1 recommended)
- git >= 1.7

Running the project
------------------------

Download the code::

    git clone git@github.com:python/raspberryio.git
    cd raspberryio

Create a virtualenv and install the necessary requirements::

    mkvirtualenv --distribute raspberryio
    $VIRTUAL_ENV/bin/pip install -r $PWD/requirements/dev.txt

Create a local settings file and set your ``DJANGO_SETTINGS_MODULE``
to use it::

    cp raspberryio/settings/local.example.py raspberryio/settings/local.py
    echo "export DJANGO_SETTINGS_MODULE=raspberryio.settings.local" >> $VIRTUAL_ENV/bin/postactivate
    echo "unset DJANGO_SETTINGS_MODULE" >> $VIRTUAL_ENV/bin/postdeactivate

Add the project directory to the virtualenv, deactivate and reactivate
it to setup the environment variables above::

    add2virtualenv .
    deactivate
    workon raspberryio

Create the Postgres database::

    createdb -E UTF-8 raspberryio

Run the initial syncdb/migrate. When asked to create a superuser,
answer ``no``. ::

    django-admin.py syncdb
    django-admin.py migrate

NOTE:
   Creating a superuser in the syncdb step will trigger the error
   ``django.db.utils.DatabaseError: relation "userprofile_profile"
   does not exist`` because of a required one-to-one relation with a
   user profile model that doesn't exist in the database yet.

**Now**, create a superuser (This will also create the profile correctly)::

    django-admin.py createsuperuser

Run the test suite with::

    django-admin.py test

You should now be able to run the development server::

    django-admin.py runserver


License
------------------------

This code is licensed under the `Apache 2.0 License
<http://www.apache.org/licenses/LICENSE-2.0.html>`_.
