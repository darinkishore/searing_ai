from .models import Document
from celery import shared_task

from rest_framework import serializers
from rest_framework import request

from rest_framework.renderers import JSONRenderer

from apps.data.models import Document, Summary, Question
from apps.api.views import DocumentViewSet

from apps.api.tasks import upload_document_task as udt


@shared_task
def process_document_task(document_id):
    document = Document.objects.get(pk=document_id)
    # call api function to process document

