from abc import ABC

import django.core.files.storage
from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


# add bucket-names to these!

class StaticStorage(S3Boto3Storage):
    location = settings.STATIC_LOCATION
    default_acl = 'public-read'


class PublicMediaStorage(S3Boto3Storage):
    location = settings.PUBLIC_MEDIA_LOCATION
    default_acl = 'public-read'
    bucket_name = 'moshimedia'
    custom_domain = f'{bucket_name}.s3.amazonaws.com'


class PrivateMediaStorage(S3Boto3Storage):
    location = settings.PRIVATE_MEDIA_LOCATION
    default_acl = 'private'
    file_overwrite = False
    bucket_name = 'moshidocs'
    custom_domain = f'{bucket_name}.s3.amazonaws.com'

