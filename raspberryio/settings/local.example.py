import sys

from raspberryio.settings.dev import *

# Override settings here

# Special test settings
if 'test' in sys.argv:
    CELERY_ALWAYS_EAGER = True

    COMPRESS_ENABLED = False
    COMPRESS_DEBUG_TOGGLE = False
    COMPRESS_CSS_COMPRESSOR = 'compressor.css.CssCompressor'
    COMPRESS_JS_COMPRESSOR = 'compressor.js.JsCompressor'
    COMPRESS_PRECOMPILERS = ()
    COMPRESS_PARSER = 'compressor.parser.AutoSelectParser'

    PASSWORD_HASHERS = (
        'django.contrib.auth.hashers.SHA1PasswordHasher',
        'django.contrib.auth.hashers.MD5PasswordHasher',
    )

    DATABASES['default']['ENGINE'] = 'django.db.backends.sqlite3'

    CACHES['default']['BACKEND'] = 'django.core.cache.backends.dummy.DummyCache'

    SOUTH_TESTS_MIGRATE = False
