import ConfigParser
import os
import random
import re
import string

from getpass import getpass

from argyle import postgres, nginx, system
from argyle.supervisor import supervisor_command, upload_supervisor_app_conf
from argyle.system import service_command

from fabric import utils
from fabric.api import cd, env, get, hide, local, put, require, run, settings, sudo, task
from fabric.contrib import files, console

# Directory structure
PROJECT_ROOT = os.path.dirname(__file__)
CONF_ROOT = os.path.join(PROJECT_ROOT, 'conf')
SERVER_ROLES = ['app', 'lb', 'db']
env.project = 'raspberryio'
env.project_user = 'raspberryio'
env.repo = u'git@github.com:python/raspberryio.git'
env.shell = '/bin/bash -c'
env.disable_known_hosts = True
env.ssh_port = 2222
env.forward_agent = True
env.password_names = ['newrelic_license_key']

# Additional settings for argyle
env.ARGYLE_TEMPLATE_DIRS = (
    os.path.join(CONF_ROOT, 'templates')
)


@task
def vagrant():
    env.environment = 'staging'
    env.vagrant = True
    env.hosts = ['33.33.33.10', ]
    env.branch = 'develop'
    env.server_name = 'vagrant.raspberry.io'
    setup_path()


@task
def staging():
    env.environment = 'staging'
    env.vagrant = False
    env.hosts = ['raspberryio-staging.caktusgroup.com', ]
    env.branch = 'develop'
    env.server_name = 'raspberryio-staging.caktusgroup.com'
    env.port = 2222
    setup_path()


@task
def production():
    env.environment = 'production'
    env.vagrant = False
    env.hosts = ['raspberry.int.python.org', ]
    env.branch = 'master'
    env.server_name = 'raspberry.io'
    # Provided machine uses default port
    env.ssh_port = 22
    setup_path()


def setup_path():
    env.home = '/home/%(project_user)s/' % env
    env.root = os.path.join(env.home, 'www', env.environment)
    env.code_root = os.path.join(env.root, env.project)
    env.project_root = os.path.join(env.code_root, env.project)
    env.virtualenv_root = os.path.join(env.root, 'env')
    env.log_dir = os.path.join(env.root, 'log')
    env.db = '%s_%s' % (env.project, env.environment)
    env.vhost = '%s_%s' % (env.project, env.environment)
    env.settings = '%(project)s.settings.%(environment)s' % env


@task
def create_users():
    """Create project user and developer users."""
    ssh_dir = u"/home/%s/.ssh" % env.project_user
    system.create_user(env.project_user, groups=['www-data', 'login', ])
    sudo('mkdir -p %s' % ssh_dir)
    user_dir = os.path.join(CONF_ROOT, "users")
    for username in os.listdir(user_dir):
        key_file = os.path.normpath(os.path.join(user_dir, username))
        system.create_user(username, groups=['dev', 'login', 'admin', ], key_file=key_file)
        with open(key_file, 'rt') as f:
            ssh_key = f.read()
        # Add ssh key for project user
        files.append('%s/authorized_keys' % ssh_dir, ssh_key, use_sudo=True)
    sudo('chown -R %s:%s %s' % (env.project_user, env.project_user, ssh_dir))


@task
def configure_ssh():
    """
    Change sshd_config defaults:
    Change default port
    Disable root login
    Disable password login
    Restrict to only login group
    """
    ssh_config = u'/etc/ssh/sshd_config'
    files.sed(ssh_config, u"Port 22$", u"Port %s" % env.ssh_port, use_sudo=True)
    files.sed(ssh_config, u"PermitRootLogin yes", u"PermitRootLogin no", use_sudo=True)
    files.append(ssh_config, u"AllowGroups login", use_sudo=True)
    files.append(ssh_config, u"PasswordAuthentication no", use_sudo=True)
    service_command(u'ssh', u'reload')


@task
def install_packages(*roles):
    """Install packages for the given roles."""
    config_file = os.path.join(CONF_ROOT, u'packages.conf')
    config = ConfigParser.SafeConfigParser()
    config.read(config_file)
    for role in roles:
        if config.has_section(role):
            # Get ppas
            if config.has_option(role, 'ppas'):
                for ppa in config.get(role, 'ppas').split(' '):
                    system.add_ppa(ppa, update=False)
            # Get sources
            if config.has_option(role, 'sources'):
                for section in config.get(role, 'sources').split(' '):
                    source = config.get(section, 'source')
                    key = config.get(section, 'key')
                    system.add_apt_source(source=source, key=key, update=False)
            sudo(u"apt-get update")
            sudo(u"apt-get install -y %s" % config.get(role, 'packages'))
            sudo(u"apt-get upgrade -y")


@task
def setup_server(*roles):
    """Install packages and add configurations for server given roles."""
    require('environment')
    # Set server locale
    sudo('/usr/sbin/update-locale LANG=en_US.UTF-8')
    roles = list(roles)
    if roles == ['all', ]:
        roles = SERVER_ROLES
    if 'base' not in roles:
        roles.insert(0, 'base')
    install_packages(*roles)
    if 'db' in roles:
        if console.confirm(u"Do you want to reset the Postgres cluster?.", default=False):
            # Ensure the cluster is using UTF-8
            pg_version = postgres.detect_version()
            sudo('pg_dropcluster --stop %s main' % pg_version, user='postgres')
            sudo('pg_createcluster --start -e UTF-8 --locale en_US.UTF-8 %s main' % pg_version,
                 user='postgres')
        postgres.create_db_user(username=env.project_user)
        postgres.create_db(name=env.db, owner=env.project_user)
    if 'app' in roles:
        # Create project directories and install Python requirements
        project_run('mkdir -p %(root)s' % env)
        project_run('mkdir -p %(log_dir)s' % env)
        # FIXME: update to SSH as normal user and use sudo
        # we ssh as the project_user here to maintain ssh agent
        # forwarding, because it doesn't work with sudo. read:
        # http://serverfault.com/questions/107187/sudo-su-username-while-keeping-ssh-key-forwarding
        with settings(user=env.project_user):
            # TODO: Add known hosts prior to clone.
            # i.e. ssh -o StrictHostKeyChecking=no git@github.com
            run('git clone %(repo)s %(code_root)s' % env)
            with cd(env.code_root):
                run('git checkout %(branch)s' % env)
        # Install and create virtualenv
        with settings(hide('everything'), warn_only=True):
            test_for_pip = run('which pip')
        if not test_for_pip:
            sudo("easy_install -U pip")
        with settings(hide('everything'), warn_only=True):
            test_for_virtualenv = run('which virtualenv')
        if not test_for_virtualenv:
            sudo("pip install -U virtualenv")
        project_run('virtualenv -p python2.7 --clear --distribute %s' % env.virtualenv_root)
        path_file = os.path.join(env.virtualenv_root, 'lib', 'python2.7', 'site-packages', 'project.pth')
        files.append(path_file, env.code_root, use_sudo=True)
        sudo('chown %s:%s %s' % (env.project_user, env.project_user, path_file))
        sudo('npm install less@1.3 -g')
        update_requirements()
        upload_supervisor_app_conf(app_name=u'gunicorn')
        upload_supervisor_app_conf(app_name=u'group')
        # Restart services to pickup changes
        supervisor_command('reload')
        supervisor_command('restart %(environment)s:*' % env)
    if 'lb' in roles:
        nginx.remove_default_site()
        nginx.upload_nginx_site_conf(site_name=u'%(project)s-%(environment)s.conf' % env)


def project_run(cmd):
    """ Uses sudo to allow developer to run commands as project user."""
    sudo(cmd, user=env.project_user)


def _random_password(length=8, chars=string.letters + string.digits):
    """Generates a random password with the specificed length and chars."""
    return ''.join([random.choice(chars) for i in range(length)])


def _load_passwords(names, length=20, generate=False):
    """Retrieve password from the user's home directory, or generate a new random one if none exists"""
    for name in names:
        filename = ''.join([env.home, name])
        if generate:
            passwd = _random_password(length=length)
            sudo('touch %s' % filename, user=env.project_user)
            sudo('chmod 600 %s' % filename, user=env.project_user)
            with hide('running'):
                sudo('echo "%s">%s' % (passwd, filename), user=env.project_user)
        if env.host_string and files.exists(filename):
            with hide('stdout'):
                passwd = sudo('cat %s' % filename).strip()
        else:
            passwd = getpass('Please enter %s: ' % name)
        setattr(env, name, passwd)


@task
def update_service_confs():
    """Update supervisor configuration."""
    require('environment')
    if not env.vagrant:
        upload_newrelic_conf()
    upload_supervisor_app_conf(app_name=u'gunicorn')
    upload_supervisor_app_conf(app_name=u'group')
    nginx.upload_nginx_site_conf(site_name=u'%(project)s-%(environment)s.conf' % env)
    # Restart services to pickup changes
    supervisor_command('reload')


@task
def upload_newrelic_conf():
    """Upload New Relic configuration from the template."""
    require('environment')
    _load_passwords(env.password_names)
    template = os.path.join(CONF_ROOT, 'templates', 'newrelic.ini')
    destination = os.path.join(env.root, 'newrelic-%(environment)s.ini' % env)
    files.upload_template(template, destination, context=env, use_sudo=True)
    sudo('chown %s:%s %s' % (env.project_user, env.project_user, destination))


@task
def update_requirements():
    """Update required Python libraries."""
    require('environment')
    project_run(u'HOME=%(home)s %(virtualenv)s/bin/pip install --use-mirrors -r %(requirements)s' % {
        'virtualenv': env.virtualenv_root,
        'requirements': os.path.join(env.code_root, 'requirements', 'production.txt'),
        'home': env.home,
    })


@task
def manage_run(command):
    """Run a Django management command on the remote server."""
    require('environment')
    manage_base = u"%(virtualenv_root)s/bin/django-admin.py " % env
    if '--settings' not in command:
        command = u"%s --settings=%s" % (command, env.settings)
    project_run(u'%s %s' % (manage_base, command))


@task
def manage_shell():
    """Drop into the remote Django shell."""
    manage_run("shell")


@task
def syncdb():
    """Run syncdb and South migrations."""
    manage_run('syncdb')
    manage_run('migrate --noinput')


@task
def collectstatic():
    """Collect static files."""
    manage_run('compress')
    manage_run('collectstatic --noinput')


def match_changes(changes, match):
    pattern = re.compile(match)
    return pattern.search(changes) is not None


@task
def deploy(branch=None, full=False):
    """Deploy to a given environment."""
    require('environment')
    if branch is not None:
        env.branch = branch
    requirements = False if not full else True
    migrations = False if not full else True
    # Fetch latest changes
    with cd(env.code_root):
        with settings(user=env.project_user):
            run('git fetch origin')
        # Look for new requirements or migrations
        changes = run("git diff origin/%(branch)s --stat-name-width=9999" % env)
        requirements = match_changes(changes, r"requirements/")
        migrations = match_changes(changes, r"/migrations/")
        if requirements or migrations:
            supervisor_command('stop %(environment)s:*' % env)
        with settings(user=env.project_user):
            run("git reset --hard origin/%(branch)s" % env)
    if requirements:
        update_requirements()
        # New requirements might need new tables/migrations
        syncdb()
    elif migrations:
        syncdb()
    collectstatic()
    supervisor_command('restart %(environment)s:*' % env)


@task
def upload_secrets(secrets_filepath):
    """Upload a settings.ini file to the server"""
    require('environment')
    destination_file = os.path.join(env.root, 'settings.ini')
    put(secrets_filepath, destination_file, use_sudo=True)
    sudo('chown %s:%s %s' % (env.project_user, env.project_user, destination_file))


@task
def get_db_dump(clean=True):
    """Get db dump of remote enviroment."""
    require('environment')
    dump_file = '%(environment)s.sql' % env
    temp_file = os.path.join(env.home, dump_file)
    flags = '-Ox'
    if clean:
        flags += 'c'
    sudo('pg_dump %s %s > %s' % (flags, env.db, temp_file), user=env.project_user)
    get(temp_file, dump_file)


@task
def load_db_dump(dump_file):
    """Load db dump on a remote environment."""
    require('environment')
    temp_file = os.path.join(env.home, '%(environment)s.sql' % env)
    put(dump_file, temp_file, use_sudo=True)
    sudo('psql -d %s -f %s' % (env.db, temp_file), user=env.project_user)


@task
def reset_local_media():
    """ Reset local media from remote host """

    require('environment', provided_by=('staging', 'production'))
    media = os.path.join(env.code_root, 'public/media')
    local("rsync -rvaze 'ssh -p %s' %s@%s:%s %s/public" %
        (env.ssh_port, env.user, env.hosts[0], media, PROJECT_ROOT))


@task
def reset_local_db():
    """ Reset local database from remote host """
    require('code_root', provided_by=('production', 'staging'))
    question = 'Are you sure you want to reset your local ' \
               'database with the %(environment)s database?' % env
    if not console.confirm(question, default=False):
        utils.abort('Local database reset aborted.')
    if env.environment == 'staging':
        from raspberryio.settings.staging import DATABASES as remote
    else:
        from raspberryio.settings.production import DATABASES as remote
    from raspberryio.settings.local import DATABASES as loc
    local_db = loc['default']['NAME']
    remote_db = remote['default']['NAME']
    with settings(warn_only=True):
        local('dropdb %s' % local_db)
    local('createdb %s' % local_db)
    host = '%s@%s' % (env.project_user, env.hosts[0])
    local('ssh -p %s -C %s pg_dump -Ox %s | psql %s' % (env.ssh_port, host, remote_db, local_db))
