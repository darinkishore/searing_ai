import os
import time

import boto3
from celery import shared_task, Celery
from apps.data.models import Document, Summary, Question
import sentry_sdk
from sentry_sdk.integrations.celery import CeleryIntegration

app = Celery('searing_ai')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

sentry_sdk.init(
    dsn='https://1a8f8766036f40e2af0f57c926013e39@o4503939342532608.ingest.sentry.io/4503954325897216',
    integrations=[
        CeleryIntegration(),
    ],

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production,
    traces_sample_rate=1.0,
)

@app.task
def wait_for_text_extraction_task(document_id):
    """
    Wait for text extraction to finish.
    """
    
    # TODO: fix the waiting 5 seconds for long enough causes recursion that's too big for memory bug
    document = Document.objects.get(id=document_id)
    response = document.get_text_extraction()
    if response != 'DONE':
        time.sleep(5)
        wait_for_text_extraction_task(document_id)
    else:
        extract_text_task(document_id)

@app.task
def start_text_extraction_task(document_id):
    document = Document.objects.get(pk=document_id)
    document.start_text_extraction()
    wait_for_text_extraction_task(document_id)

@app.task
def extract_text_task(document_id):
    document = Document.objects.get(pk=document_id)
    document.extract_text()
    create_summary_task(document_id)
    create_questions_task(document_id)

@app.task
def create_summary_task(document_id):
    document = Document.objects.get(pk=document_id)
    document.create_summary()

@app.task
def create_questions_task(document_id):
    document = Document.objects.get(pk=document_id)
    document.create_questions()
