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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.access_key = os.environ.get('AWS_ACCESS_KEY_ID')
        self.secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')

    file_overwrite = False



