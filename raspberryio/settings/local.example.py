import sys

from raspberryio.settings.dev import *

# Override settings here

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
