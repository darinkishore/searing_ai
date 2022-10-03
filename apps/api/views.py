import os
import environ
import boto3
import re
import requests
from django.shortcuts import get_object_or_404, redirect

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.generics import GenericAPIView
from rest_framework import viewsets

from apps.api.permissions import IsAuthenticatedOrHasUserAPIKey
from apps.data.tasks import start_text_extraction_task
from apps.users.models import CustomUser
from apps.data.models import Document, Summary, Question
from apps.api.serializers import DocumentSerializer, SummarySerializer, QuestionSerializer, UserSerializer, \
    DocumentFormSerializer

# basic CRUD classes for users, documents, summaries, and questions

IS_AUTHORIZED = [SessionAuthentication, BasicAuthentication]


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows users to be viewed.
    """
    authentication_classes = IS_AUTHORIZED
    permission_classes = [IsAdminUser]

    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

class DocumentForm(GenericAPIView):
    """
    API endpoint that allows documents to be created.
    """
    # authentication_classes, permission_classes = IS_AUTHORIZED, IsAuthenticatedOrHasUserAPIKey

    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'api/api_form.html'
    serializer_class = DocumentFormSerializer
    parser_classes = MultiPartParser, JSONParser

    def get(self, request, *args, **kwargs):
        serializer = DocumentFormSerializer()
        return Response({'serializer': serializer})

    def post(self, request):
        serializer = DocumentFormSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return redirect(reverse('DocumentForm'))
        else:
            return Response({'serializer': serializer})


class DocumentViewSet(viewsets.ModelViewSet):
    """
    Allows you to list, create, retrieve, update, and destroy documents.
    """
    authentication_classes = IS_AUTHORIZED
    permission_classes = [IsAuthenticatedOrHasUserAPIKey]

    parser_classes = (MultiPartParser, FormParser)
    serializer_class = DocumentSerializer

    def perform_create(self, serializer):
        # create a document and set its id
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Document.objects.filter(user=self.request.user)

    def get_object(self):
        return get_object_or_404(Document, pk=self.kwargs['pk'])

    @action(detail=True, methods=['get'])
    def start_summary_generation(self, request, pk=None):
        start_text_extraction_task(pk)



class SummaryViewSet(viewsets.ModelViewSet):
    """
    Allows you to list, create, retrieve, update, and destroy
    a document's one summary.
    """
    authentication_classes = IS_AUTHORIZED
    permission_classes = [IsAuthenticatedOrHasUserAPIKey]
    serializer_class = SummarySerializer

    def get_queryset(self):
        # Show only the summary for the document that the user owns
        return Summary.objects.filter(document__user=self.request.user,
                                      document__id=self.kwargs['document_id']).first()


class QuestionViewSet(viewsets.ModelViewSet):
    """
    Allows you to list, create, retrieve, update, and destroy questions.
    """
    authentication_classes = IS_AUTHORIZED
    permission_classes = [IsAuthenticatedOrHasUserAPIKey]
    serializer_class = QuestionSerializer

    def get_queryset(self):
        # Show only the questions for the current document
        return Question.objects.filter(document__user=self.request.user,
                                       document__id=self.kwargs['document_id'])
