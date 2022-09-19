from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase


import rest_framework.test as rest_test
from apps.data.models import Document, Summary, Question, CustomUser
from apps.api.views import DocumentViewSet, SummaryViewSet, QuestionViewSet, UserViewSet

from apps.data.storage_backends import PrivateMediaStorage

# tests our API views
class TestDocumentViewSet(TestCase):
    def setUp(self):
        self.factory = rest_test.APIRequestFactory()
        self.user = get_user_model().objects.create_user(
            username='testuser')
        self.user.set_password('12345')
        self.user.save()
        self.client = rest_test.APIClient()
        self.client.force_authenticate(user=self.user)
        self.document = Document.objects.create(
            user=self.user,
            title='test document',
            file=SimpleUploadedFile(
                'test.pdf',
                b'file_content',
                content_type='application/pdf',
            )
        )
        self.summary = Summary.objects.create(
            document=self.document,
            content='test summary'
        )
        self.question = Question.objects.create(
            document=self.document,
            question='test question',
            answer='test answer'
        )
        self.document.save()
        self.summary.save()
        self.question.save()

    def test_document_list(self):
        request = self.factory.get('/documents/')
        view = DocumentViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['title'], 'test document')
        self.assertEqual(response.data['results'][0]['user'], self.user.id)
        self.assertEqual(response.data['results'][0]['document'], 'test.pdf')

    def test_document_create(self):
        request = self.factory.post('/documents/', {
            'title': 'test document 2',
            'document': SimpleUploadedFile(
                'test2.pdf',
                b'file_content',
                content_type='application/pdf',
            )
        })
        view = DocumentViewSet.as_view({'post': 'create'})
        response = view(request)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['title'], 'test document 2')
        self.assertEqual(response.data['user'], self.user.id)
        self.assertEqual(response.data['document'], 'test2.pdf')

    def test_document_update(self):
        request = self.factory.put('/documents/1/', {
            'title': 'test document 3',
            'document': SimpleUploadedFile(
                'test3.pdf',
                b'file_content',
                content_type='application/pdf',
            )
        })
        view = DocumentViewSet.as_view({'put': 'update'})
        response = view(request, pk=1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], 'test document 3')
        self.assertEqual(response.data['user'], self.user.id)
        self.assertEqual(response.data['document'], 'test3.pdf')

    def test_document_delete(self):
        request = self.factory.delete('/documents/1/')
        view = DocumentViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=1)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Document.objects.count(), 0)

