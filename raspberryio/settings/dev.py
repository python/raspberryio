from raspberryio.settings.base import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

MIDDLEWARE_CLASSES += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

INSTALLED_APPS += (
    'debug_toolbar',
)

INTERNAL_IPS = ('127.0.0.1', )

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False
}


COMPRESS_ENABLED = False

CELERY_ALWAYS_EAGER = True

# Testing
SOUTH_TESTS_MIGRATE = True

TEST_RUNNER = 'hilbert.test.CoverageRunner'

DEFAULT_TEST_LABELS = ['project', 'userprofile', 'search', 'qanda']

COVERAGE_MODULES = (
    'forms',
    'models',
    'views',
    'utils',
)
