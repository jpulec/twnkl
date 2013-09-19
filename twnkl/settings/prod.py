from common import *
from storages.backends.s3boto import S3BotoStorage
import dj_database_url

DEBUG= True
TEMPLATE_DEBUG=True

DATABASES['default'] = dj_database_url.config()

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

ALLOWED_HOSTS = ['*']

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
AWS_STORAGE_BUCKET_NAME = 'twnkl'

S3_URL = 'https://%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
STATIC_URL = MEDIA_URL = S3_URL

STATIC_URL += "static/"
MEDIA_URL += "media/"

INSTALLED_APPS += ('gunicorn', 'storages', 'raven.contrib.django.raven_compat',)

RAVEN_CONFIG = {
            'dsn': 'https://790da17eae914050a378b2c5a8ab144c:f16e8a80844a414baa64c74682b6a8ae@app.getsentry.com/13264',
            }

LOGGING = {
        'version': 1,
        'disable_existing_loggers': True,
        'root': {
            'level': 'WARNING',
            'handlers': ['sentry'],
            },
        'formatters': {
            'verbose': {
                'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
                },
            },
        'handlers': {
            'sentry': {
                'level': 'ERROR',
                'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
                },
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'verbose'
                }
            },
        'loggers': {
            'django.db.backends': {
                'level': 'ERROR',
                'handlers': ['console'],
                'propagate': False,
                },
            'raven': {
                'level': 'DEBUG',
                'handlers': ['console'],
                'propagate': False,
                },
            'sentry.errors': {
                'level': 'DEBUG',
                'handlers': ['console'],
                'propagate': False,
                },
            },
        }
