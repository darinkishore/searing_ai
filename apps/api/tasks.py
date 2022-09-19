import os

import boto3

from apps.data.models import Document, Summary, Question
from celery import shared_task

import environ
from searing_ai.settings import BASE_DIR

from .views import DocumentViewSet

# get environment variables

env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))


@shared_task
def process_document(document: Document):
    # create a textract client
    textract = boto3.client \
        ('textract',
         aws_access_key_id=env('AWS_ACCESS_KEY_ID'),
         aws_secret_access_key=env('AWS_SECRET_ACCESS_KEY'),
         region_name=env('AWS_REGION_NAME'))

    # call Amazon Textract
    response = textract.detect_document_text(Document={'Bytes': document.file.read()})

def upload_document_task(request):
    """
    Uploads given to Amazon S3 asynchronously by
    sending a post request to the backend API app.
    """
    DocumentViewSet.as_view({'post': 'create'})(request)
