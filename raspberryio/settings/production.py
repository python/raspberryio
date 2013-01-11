from raspberryio.settings.staging import *

# There should be only minor differences from staging

DATABASES['default']['NAME'] = 'raspberryio_production'

EMAIL_SUBJECT_PREFIX = '[Raspberryio Prod] '

