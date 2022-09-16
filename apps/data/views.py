from django.contrib.auth.decorators import login_required

from django.shortcuts import render, get_object_or_404
from django.contrib import messages

from .forms import DocumentForm

# Create your views here.
# views are functions that take in request and return http response

# views should handle presentation logic -> what to show to the user
# views should not handle business logic -> what to do with the data
#   -> business logic should be handled in models (or forms)

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
            form = DocumentForm()  # clear form
        response = render(request, 'data/document_form.html', {'form': form})
        if success:
            messages.success(request, 'Document uploaded successfully')
        else:
            messages.error(request, 'Document upload failed')
        return response
