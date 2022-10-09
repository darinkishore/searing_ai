import os
from abc import ABC

import django.core.files.storage
from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage, S3StaticStorage



# add bucket-names to these!

class PublicMediaStorage(S3Boto3Storage):
    AWS_S3_ACCESS_KEY_ID = settings.AWS_ACCESS_KEY_ID
    AWS_S3_SECRET_ACCESS_KEY = settings.AWS_SECRET_ACCESS_KEY
    location = settings.PUBLIC_MEDIA_LOCATION

    bucket_name = 'moshimedia'
    custom_domain = f'{bucket_name}.s3.amazonaws.com'


class PrivateMediaStorage(S3Boto3Storage):
    access_key = os.environ.get('AWS_ACCESS_KEY_ID')
    secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')

    location = settings.PRIVATE_MEDIA_LOCATION

    default_acl = 'private'

    file_overwrite = False
    bucket_name = 'moshimedia'
    custom_domain = f'{bucket_name}.s3.amazonaws.com'


