import sys

from raspberryio.settings.dev import *

## Override settings here

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'yv!hkvt&amp;k8dn^$*$&amp;lif)#ydw8zvk4iz93s8m+$x%eyg-!$n69'


# Special test settings
if 'test' in sys.argv:
    CELERY_ALWAYS_EAGER = True

    COMPRESS_ENABLED = False
    PASSWORD_HASHERS = (
        'django.contrib.auth.hashers.SHA1PasswordHasher',
        'django.contrib.auth.hashers.MD5PasswordHasher',
    )

    DATABASES['default']['ENGINE'] = 'django.db.backends.sqlite3'

    CACHES['default']['BACKEND'] = 'django.core.cache.backends.dummy.DummyCache'

    SOUTH_TESTS_MIGRATE = False
