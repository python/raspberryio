.. _deployment:

Deployment
==========

This section documents the process by which we deploy Raspberry IO.
This is done on a staging site first, and then to a production site
once the code is proven to be stable and working on staging.

.. Note::
   The deployment uses SSH with agent forwarding so you'll need to
   enable agent forwarding if it is not already by adding
   ``ForwardAgent yes`` to your SSH config.


Server Provisioning
-------------------

The first step in creating a new server is to create users on the remote server. You
will need root user access with passwordless sudo. How you specify this user will vary
based on the hosting provider. EC2 and Vagrant use a private key file. Rackspace and
Linode use a user/password combination.

1. For each developer, put a file in the ``conf/users`` directory
   containing their public ssh key, and named exactly the same as the
   user to create on the server, which should be the same as the
   userid on the local development system. (E.g. for user ``dickens``,
   the filename must be ``dickens``, not ``dickens.pub`` or
   ``user_dickens``.)

2. Run this command to create users on the server::

        fab -H <fresh-server-ip> -u <root-user> create_users

   This will create a project user and users for all the developers.

3. Lock down SSH connections: disable password login and move the
   default port from 22 to ``env.ssh_port``::

        fab -H <fresh-server-ip> configure_ssh

4. Add the IP to the appropriate environment function and provision it
   for its role. You can provision a new server with the
   ``setup_server`` fab command. It takes a list of roles for this
   server ('app', 'db', 'lb') or you can say 'all'. The name of the
   environment can now be used in fab commands (such as production,
   staging, and so on.) To setup a server with all roles use::

        fab staging setup_server:all

5. Deploy the latest code to the newly setup server::

        fab staging deploy

6. If a new database is desired for this environment, use ``syncdb``::

        fab staging syncdb

7. Otherwise, a database can be moved to the new environment using
   ``get_db_dump`` and ``load_db_dump`` as in the following example::

        fab production get_db_dump
        fab staging load_db_dump:production.sql


Vagrant Testing
---------------

You can test the provisioning/deployment using
`Vagrant <http://vagrantup.com/>`_. Using the Vagrantfile you can start up the
VM. This uses the ``precise64`` box::

    vagrant up

With the VM up and running, you can create the necessary users.
Put the developers' keys in ``conf/users`` as before, then
use these commands to create the users. The location of the vagrant key file might be::

    if gem installed: /usr/lib/ruby/gems/1.8/gems/vagrant-1.0.2/keys/vagrant
    if apt-get installed: /usr/share/vagrant/keys/vagrant

This may vary on your system. Running ``locate keys/vagrant`` might help find it.
Use the full path to the keys/vagrant file as the value in the ``-i`` option::

    fab -H 33.33.33.10 -u vagrant -i /usr/share/vagrant/keys/vagrant create_users
    fab vagrant setup_server:all
    fab vagrant deploy
    fab vagrant syncdb

When prompted, do not make a superuser during the syncdb, but do make a site.
To make a superuser, you'll need to run
```fab vagrant manage_run:createsuperuser```

It is not necessary to reconfigure the SSH settings on the vagrant box.

The vagrant box forwards port 80 in the VM to port 8080 on the host
box. You can view the site by visiting localhost:8080 in your browser.

You may also want to add::

    33.33.33.10 vagrant.raspberry.io

to your hosts (``/etc/hosts``) file.

You can stop the VM with ``vagrant halt`` and destroy the box
completely to retest the provisioning with ``vagrant destroy``.

For more information please review the Vagrant documentation.


Deployment
----------

For future deployments, you can deploy changes to a particular environment with
the ``deploy`` command. This takes an optional branch name to deploy. If the branch
is not given, it will use the default branch defined for this environment in
``env.branch``::

    fab staging deploy
    fab staging deploy:new-feature

New requirements or South migrations are detected by parsing the VCS changes and
will be installed/run automatically.
