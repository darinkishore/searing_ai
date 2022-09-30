import boto3
import environ

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.exceptions import ValidationError
from ..api.serializers import DocumentSerializer

from django.urls import reverse

from rest_framework import request

from PyPDF2 import PdfFileWriter, PdfFileReader

# import boto3 for amazon textract

from apps.api import views as api
from .tasks import start_text_extraction_task
from ..web.views import home as web_home
from .forms import DocumentForm
from .models import Document, Summary, Question

# Create your views here.
# views are functions that take in request and return http response

# views should handle presentation logic -> what to show to the user
# views should not handle business logic -> what to do with the data
#   -> business logic should be handled in models (or forms)



@login_required
def home(request):
    return web_home(request)


# shows a table of documents with links to summary and questions
@login_required
def doc_table(request):
    if request.method == 'GET':
        documents = Document.objects.filter(user=request.user).order_by('-created_at')
        return render(request, 'data/doc_table.html', {'documents': documents})


# displays a form to upload a document
@login_required
def upload(request):
    if request.method == 'GET':
        return render(request, 'data/document_form.html', {'form': DocumentForm()})

    if request.method == 'POST':
        doc = Document(user=request.user, title=request.POST['title'], file=request.FILES['file.0'])
        try:
            doc.full_clean()
            doc.save()
            start_text_extraction_task.delay(doc.id)
            messages.success(request, 'Document is processing! Please check back later. :)')
        except ValidationError as e:
            messages.error(request, e)

        return redirect('data:upload')




@login_required
def summary_view(request, pk):
    document = get_object_or_404(Document, pk=pk)
    summary = Summary.objects.filter(document=document).first()
    return render(request, 'data/summary.html', {'summary': summary})


@login_required
def questions_view(request, pk):
    document = get_object_or_404(Document, pk=pk)
    questions = list(Question.objects.filter(document=document))
    return render(request, 'data/questions.html', {'questions': questions})