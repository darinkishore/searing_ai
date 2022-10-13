import os

import boto3

from apps.data.models import Document, Summary, Question
from celery import shared_task

import environ
from searing_ai.settings import BASE_DIR

from .views import DocumentViewSet
