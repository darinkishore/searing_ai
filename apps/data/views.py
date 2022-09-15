from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Sum, Count
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.templatetags.static import static
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST, require_http_methods
from django.views.generic import TemplateView
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.api.helpers import get_user_from_request
from apps.api.permissions import IsAuthenticatedOrHasUserAPIKey

from .models import Document, Summary, Questions


# Create your views here.
# views are functions that take in request and return http response

# views should handle presentation logic -> what to show to the user
# views should not handle business logic -> what to do with the data
#   -> business logic should be handled in models (or forms)

@login_required
def upload(request):
    # if request.method == 'POST':
    return NotImplementedError

