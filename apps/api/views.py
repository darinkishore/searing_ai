import os
import environ
import boto3
import re
import requests
from django.shortcuts import get_object_or_404

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import viewsets

from apps.users.models import CustomUser
from apps.data.models import Document, Summary, Question
from apps.api.serializers import DocumentSerializer, SummarySerializer, QuestionSerializer, UserSerializer

# boto3 client init for textract
env = environ.Env()
environ.Env.read_env()
AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
AWS_REGION = env('AWS_REGION')

textract = boto3.client('textract', aws_access_key_id=AWS_ACCESS_KEY_ID,
                        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                        region_name=AWS_REGION)

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


class DocumentViewSet(viewsets.ModelViewSet):
    """
    Allows you to list, create, retrieve, update, and destroy documents.
    """
    authentication_classes = IS_AUTHORIZED
    permission_classes = [IsAuthenticated]

    parser_classes = (MultiPartParser, FormParser)
    serializer_class = DocumentSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Document.objects.filter(user=self.request.user)

    def get_object(self):
        return get_object_or_404(Document, pk=self.kwargs['pk'])

    @action(detail=True, methods=['get'])
    def start_doc_text_detection(self, request, *args, **kwargs):
        """
        Process a document via Amazon Textract to get its contents.
        """
        doc = self.get_object()
        name = 'private/' + doc.file.name
        # make a boto3 s3 client to get the file from a user's private s3 bucket
        s3 = boto3.resource('s3', aws_access_key_id=env('DO_ACCESS_KEY_ID'),
                            aws_secret_access_key=env('DO_SECRET_ACCESS_KEY'),
                            endpoint_url=env('DO_S3_ENDPOINT_URL'))

        s3_object = s3.Object(bucket_name=env('DO_STORAGE_BUCKET_NAME'), key=name)

        job_id = textract.start_document_text_detection(
            DocumentLocation={
                'S3Object': s3_object
            })

        return job_id

    @action(detail=True, methods=['get'])
    def get_doc_text(job_id):
        """
        Get the text from a document.
        """
        response = textract.get_document_text_detection(JobId=job_id)
        return response


class SummaryViewSet(viewsets.ModelViewSet):
    """
    Allows you to list, create, retrieve, update, and destroy
    a document's one summary.
    """
    authentication_classes = IS_AUTHORIZED
    permission_classes = [IsAuthenticated]
    serializer_class = SummarySerializer

    def create_summary(self, document):
        """
        Create a summary for a document.
        """
        pass

    def get_queryset(self):
        # Show only the summary for the document that the user owns
        return Summary.objects.filter(document__user=self.request.user)


class QuestionViewSet(viewsets.ModelViewSet):
    """
    Allows you to list, create, retrieve, update, and destroy questions.
    """
    authentication_classes = IS_AUTHORIZED
    permission_classes = [IsAuthenticated]
    serializer_class = QuestionSerializer

    def get_queryset(self):
        # Show only the questions for the document that the user owns
        return Question.objects.filter(document__user=self.request.user)
