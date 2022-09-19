import os

from django.contrib.auth.decorators import login_required

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import permission_classes, api_view, action
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, mixins, generics
from rest_framework.reverse import reverse
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
        doc = Document.objects.get_object_or_404(self.get_queryset(), user=self.request.user, id=self.kwargs['pk'])
        self.check_object_permissions(self.request, doc)
        return doc

    # this method should eventually POST a summary
    @action(detail=True, methods=['get'])
    def process_document(self):
        """
        Process a document via Amazon Textract to get its contents.
        """
        tasks.process_document.delay(self.get_object())


class SummaryViewSet(viewsets.ModelViewSet):
    """
    Allows you to list, create, retrieve, update, and destroy
    a document's one summary.
    """
    authentication_classes = IS_AUTHORIZED
    permission_classes = [IsAuthenticated]
    serializer_class = SummarySerializer

    def get_queryset(self):
        # Show only the summary for the document that the user owns
        return Summary.objects.filter(document__user=self.request.user, document__id=self.kwargs['document_pk'])

    def get_object(self):
        summary = Summary.objects.get_object_or_404(self.get_queryset(), id=self.kwargs['pk'])
        self.check_object_permissions(self.request, summary)
        return summary


class QuestionViewSet(viewsets.ModelViewSet):
    """
    Allows you to list, create, retrieve, update, and destroy questions.
    """
    authentication_classes = IS_AUTHORIZED
    permission_classes = [IsAuthenticated]
    serializer_class = QuestionSerializer

    def get_queryset(self):
        # Show only the questions for the document that the user owns
        return Question.objects.filter(document__user=self.request.user, document__id=self.kwargs['document_pk'])

    def get_object(self):
        question = Question.objects.get_object_or_404(self.get_queryset())
        self.check_object_permissions(self.request, question)
        return question
