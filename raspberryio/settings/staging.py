import json
import os

from ConfigParser import RawConfigParser

from raspberryio.settings.base import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
        ('RaspberryIO Team', 'raspberryio-team@caktusgroup.com'),
    )
MANAGERS = ADMINS

DATABASES['default']['NAME'] = 'raspberryio_staging'

INSTALLED_APPS += (
    'gunicorn',
)

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

EMAIL_SUBJECT_PREFIX = '[Raspberryio Staging] '

########## COMPRESSION CONFIGURATION
COMPRESS_ENABLED = False
# Default : the opposite of DEBUG

COMPRESS_OFFLINE = False

COMPRESS_DEBUG_TOGGLE = 'compressor'
COMPRESS_JS_COMPRESSOR = 'compressor.css.CssCompressor'
COMPRESS_CSS_COMPRESSOR = 'compressor.js.JsCompressor'
COMPRESS_OUTPUT_DIR = 'CACHE'
COMPRESS_JS_FILTERS = 'compressor.filters.jsmin.JSMinFilter'
COMPRESS_CSS_FILTERS = 'compressor.filters.css_default.CssAbsoluteFilter'
########## END COMPRESSION CONFIGURATION

# import secrets
try:
    SECRETS_ROOT = os.path.abspath(os.path.join(PROJECT_ROOT, os.pardir))
    config = RawConfigParser()
    config.read(os.path.join(SECRETS_ROOT, 'settings.ini'))
    SUPERFEEDR_CREDS = json.loads(config.get('secrets', 'SUPERFEEDR_CREDS'))
except:
    pass
