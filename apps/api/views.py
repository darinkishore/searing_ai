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
