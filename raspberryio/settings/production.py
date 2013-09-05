import json
import os

from ConfigParser import RawConfigParser

from raspberryio.settings.staging import *

# import secrets
try:
    SECRETS_ROOT = os.path.abspath(os.path.join(PROJECT_ROOT, os.pardir))
    config = RawConfigParser()
    config.read(os.path.join(SECRETS_ROOT, 'settings.ini'))
    SUPERFEEDR_CREDS = json.loads(config.get('secrets', 'SUPERFEEDR_CREDS'))
    SECRET_KEY = json.loads(config.get('secrets', 'SECRET_KEY'))
    DATABASES['default']['NAME'] = config.get('database', 'DATABASE_NAME')
    DATABASES['default']['HOST'] = config.get('database', 'DATABASE_HOST')
    DATABASES['default']['USER'] = config.get('database', 'DATABASE_USER')
    DATABASES['default']['PASSWORD'] = config.get('database', 'DATABASE_PASSWORD')

except:
    pass

EMAIL_SUBJECT_PREFIX = '[Raspberryio Prod] '

# Disqus
DISQUS_SHORTNAME = 'raspberryio'
