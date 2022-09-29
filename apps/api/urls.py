from django.urls import path, include
from . import views
from rest_framework import routers

app_name = 'api'

router = routers.DefaultRouter(trailing_slash=False)

# we are trying to have a urlconfig that goes
# /api/documents/1/summary/
# /api/documents/1/questions/
router.register(r'documents', views.DocumentViewSet, basename='documents')
router.register(r'documents/(?P<document_id>\d+)/summary', views.SummaryViewSet, basename='summary')
router.register(r'documents/(?P<document_id>\d+)/questions', views.QuestionViewSet, basename='questions')

# only admin accessible route:
router.register(r'users', views.UserViewSet, basename='users')



urlpatterns = [
    path('doc-form', views.DocumentForm.as_view(), name='doc-form'),
    path('', include(router.urls)),
]

