from common import *
from storages.backends.s3boto import S3BotoStorage

StaticRootS3BotoStorage = lambda: S3BotoStorage(location='static')
MediaRootS3BotoStorage = lambda: S3BotoStorage(location='media')

import dj_database_url
DATABASES['default'] = dj_database_url.config()

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

ALLOWED_HOSTS = ['*']

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
AWS_STORAGE_BUCKET_NAME = os.environ['AWS_STORAGE_BUCKET_NAME']

STATICFILES_STORAGE = StaticRootS3BotoStorage
DEFAULT_FILE_STORAGE = MediaRootS3BotoStorage

S3_URL = 'https://%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
STATIC_URL = MEDIA_URL = S3_URL

STATIC_URL += "static/"
MEDIA_URL += "media/"

INSTALLED_APPS += ('gunicorn', 'storages',)
