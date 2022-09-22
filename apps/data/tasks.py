import time
from celery import shared_task, Celery
from apps.data.models import Document, Summary, Question

app = Celery('searing_ai')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.task
def wait_for_text_extraction_task(document_id):
    """
    Wait for text extraction to finish.
    """
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
    return True
