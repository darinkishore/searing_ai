import os
from abc import ABC

import django.core.files.storage
from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage, S3StaticStorage



# add bucket-names to these!

class PublicMediaStorage(S3Boto3Storage):

    location = settings.PUBLIC_MEDIA_LOCATION

    bucket_name = 'moshimedia'
    custom_domain = f'{bucket_name}.s3.amazonaws.com'


class PrivateMediaStorage(S3Boto3Storage, ABC):
    # override the access key and secret key
    # default_acl = 'private'
    location = settings.PRIVATE_MEDIA_LOCATION
    bucket_name = 'moshimedia'
    custom_domain = f'{bucket_name}.s3.amazonaws.com'

    file_overwrite = False
