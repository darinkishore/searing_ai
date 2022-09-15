from django.urls import path
from django.views.generic import TemplateView
from rest_framework import routers

from . import views

app_name = 'data'

urlpatterns = [
    path('upload/', views.upload, name='upload')
]
