from django.contrib.auth.decorators import login_required

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone

from .forms import DocumentForm
from .models import Document, Summary, Question

# Create your views here.
# views are functions that take in request and return http response

# views should handle presentation logic -> what to show to the user
# views should not handle business logic -> what to do with the data
#   -> business logic should be handled in models (or forms)

@login_required
def home(request):
    return render(request, 'web/app_home.html')


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
        form = DocumentForm(request.POST, request.FILES)
        success = False
        print(form.errors)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.title = request.POST['title']
            doc.document = request.FILES['file']
            doc.user = request.user
            doc.save()
            success = True
        if success:
            messages.success(request, 'Document uploaded successfully')
        else:
            messages.error(request, 'Document upload failed')
        # redirect to home view
        return redirect('data:upload')

@login_required
def summary_view(request, pk):
    document = get_object_or_404(Document, pk=pk)
    summary = Summary.objects.filter(document=document).first()
    return render(request, 'data/summary.html', {'summary': summary})


# TODO: change to question
@login_required
def questions_view(request, pk):
    document = get_object_or_404(Document, pk=pk)
    questions = list(Question.objects.filter(document=document))
    return render(request, 'data/questions.html', {'questions': questions})
