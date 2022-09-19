from .models import Document
from celery import shared_task

from rest_framework import serializers
from rest_framework import request

from rest_framework.renderers import JSONRenderer

from apps.data.models import Document, Summary, Question
from apps.api.views import DocumentViewSet

from apps.api.tasks import upload_document_task as udt


@shared_task
def upload_document_task(document, request):
    """
    Uploads given to Amazon S3 asynchronously by
    sending a post request to the backend API app.
    """
    udt(request)


