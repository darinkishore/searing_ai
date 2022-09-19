from django.test import TestCase

# Create your tests here.

# write tests for the following:
#   - upload a document
#   - view a document


from django.test import TestCase
from django.urls import reverse
from .models import Document, Summary, Question
from apps.users.models import CustomUser
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

# write a test to see if a user can upload a document.
# get the document
class DocumentTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user()
        self.user.save()
        self.client.force_login(self.user)
        self.document = Document.objects.create(
            title='test',
            document=SimpleUploadedFile('test.txt', b'test'),
            user=self.user
        )
        self.document.save()

    def test_document_upload(self):
        self.assertEqual(self.document.title, 'test')
        self.assertEqual(self.document.document.name, 'test.txt')
        self.assertEqual(self.document.user, self.user)

    def test_document_view(self):
        response = self.client.get(reverse('data:doc_table'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'data/doc_table.html')
        self.assertContains(response, 'test')
        self.assertContains(response, 'test.txt')


