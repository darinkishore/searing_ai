from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase


import rest_framework.test as rest_test
from apps.data.models import Document, Summary, Question, CustomUser
from apps.api.views import DocumentViewSet, SummaryViewSet, QuestionViewSet, UserViewSet

from apps.data.storage_backends import PrivateMediaStorage

# test that one user cannot retrieve another user's info/docs

