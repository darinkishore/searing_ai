import os
import time

from django.core.files import File
from django.test import TestCase, Client
from django.conf import settings

from rest_framework.test import RequestsClient
from requests.auth import HTTPBasicAuth
from rest_framework import status
from django.urls import reverse

from ..models import Document, Summary, Question
from ..storage_backends import PrivateMediaStorage
from ...users.models import CustomUser


# where did things go wrong in production?
# see if you can fetch the api and get docs
# celery needs tests :(

class TestDocument(TestCase):
    def setUp(self):
        settings.DEFAULT_FILE_STORAGE = 'data.storage_backends.PrivateMediaStorage'
        settings.STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
        settings.WHITENOISE_MANIFEST_STRICT = False
        # check to see if test_file.pdf is in private media storage

        self.client = Client()
        self.user = CustomUser.objects.create(username='test_user', password='test_password')
        # upload document to s3 bucket
        # test_file fills document.file filefield
        self.document = Document.objects.create(title='test_document', user=self.user)

        with open('test_file.pdf', 'rb') as test_file:
            self.document.file.save('test_file.pdf', File(test_file))
        self.document.save()

        self.user2 = CustomUser.objects.create(username='test_user_2', password='test_password_2')
        self.document2 = Document.objects.create(title='test_document_2', user=self.user2)
        with open('test_file_2.pdf', 'rb') as test_file:
            self.document2.file.save('test_file_2.pdf', File(test_file))
        self.document2.save()


    # see if a document can be created
    def test_document_creation(self):
        self.assertEqual(self.document.title, 'test_document')
        self.assertEqual(self.document.file, 'documents/test_file.pdf')
        self.assertEqual(self.document.user, self.user)

        self.assertEqual(self.document2.title, 'test_document_2')
        self.assertEqual(self.document2.file, 'documents/test_file_2.pdf')
        self.assertEqual(self.document2.user, self.user2)

    def test_document_ocr(self):
        self.document.start_text_extraction()
        response = self.document.get_text_extraction()
        while response != 'DONE':
            time.sleep(2)
            response = self.document.get_text_extraction()
        self.document.extract_text()
        assert self.document.text
        self.doc_summary()
        self.doc_questions()

    def doc_summary(self):
        # depends on ocr being done
        self.document.create_summary()
        assert self.document.summary
        assert self.document.summary.get_summary

    def doc_questions(self):
        self.document.create_questions()
        assert self.document.questions

    def tearDown(self) -> None:
        self.document.file.delete()
        self.document2.file.delete()
        # see if the file was deleted in s3 bucket
        self.assertFalse(self.document.file)
        self.assertFalse(self.document2.file)
        self.user.delete()
        self.user2.delete()
        self.document.delete()
        self.document2.delete()

"""
something that might help you get your integration tests (functional / end-to-end / whatever you want to call them) 
going might be something like `factory_boy` (pretty much the defacto standard for most people) or another library 
like `mixer` or `model_baker` (formerly `model_mommy`).

Depending on your model structure, you can spin up many models (perhaps a whole apps worth) in like 1 line of code. 
Tie that in with selenium for browser testing and you have very easy way to get testing your app from a users perspective.

Then you can assert that you're using the right templates, that certain key elements exist, that things are certain sizes in various situations, 
pretty much anything that might be worth testing, really. Click this, navigate there, submit that form, etc.
Additionally, we've gone the route of bringing everything over to pytest because it even gives us the ability
to allow for `--nomigrations`, which is supremely useful should you have an app with unmanaged models (which we do). 
While it is possible to do that in Django, you have to come up with some wonky/hacky workarounds - whereas with pytest
you just pass it that option.

"""

"""
    # see if the ocr is successfully generated
    def test_document_ocr(self):
        self.document.start_text_extraction()
        while self.document.get_text_extraction(self.document.job_id) != 'DONE':
            time.sleep(2)
            if self.document.get_text_extraction(self.document.job_id) == 'FAILED':
                assert False
        self.document.get_text_extraction()
        self.document.extract_text()
        assert self.document.text

    # see if there is a summary generated
    def test_document_summary(self):
        # depends on ocr being done
        if self.document.get_text_extraction(self.document.job_id) == 'DONE':
            self.document.create_summary()
            assert self.document.summary
            assert self.document.summary.get_summary
        else:
            self.document.start_text_extraction()
            while self.document.get_text_extraction(self.document.job_id) != 'DONE':
                time.sleep(2)
        self.document.get_text_extraction()
        self.document.extract_text()
        self.document.create_summary()

    # see if there are questions generated
    def test_document_questions(self):
        # depends on ocr being done
        if self.document.get_text_extraction(self.document.job_id) == 'DONE':
            # depends on summary being done
            if self.document.summary:
                self.document.create_questions()
                assert self.document.questions
            else:
                self.document.create_summary()
                self.document.create_questions()
        else:
            self.document.start_text_extraction()
            while self.document.get_text_extraction(self.document.job_id) != 'DONE':
                time.sleep(2)

        assert self.document.questions

    # see if a user can access their own documents and not another user's documents
    def test_document_access(self):
        # on lockdown/form.html, enter the lockdown password

        # create new api client
        api_client = APIClient()
        # login as user1
        api_client.force_authenticate(user=self.user)
        # get user1's documents
        response = api_client.get('/api/documents')
        # ensure user1 can access their own documents
        assert response.status_code == 200
        assert response.data['count'] == 1
        # try to get user2's documents
        response = api_client.get('/api/documents/' + str(self.document2.id))
        # ensure user1 cannot access user2's documents
        assert response.status_code == 404
        # logout
        api_client.logout()

        # login as user2
        api_client.force_authenticate(user=self.user2)
        # get user2's documents
        response = api_client.get('/api/documents')
        # ensure user2 can access their own documents
        assert response.status_code == 200
        assert response.data[0]['title'] == 'test_document2'
        # logout
        api_client.logout()

        # other edge cases for access:
        # 1. user is not logged in
        api_client.force_authenticate(user=None)
        response = api_client.get('/api/documents')
        assert response.status_code == 401
        # 2. user is logged in but not the owner of the document
        api_client.force_authenticate(user=self.user2)
        response = api_client.get('/api/documents/' + str(self.document.id))
        assert response.status_code == 404
        # 3. user is logged in but not the owner of the summary
        response = api_client.get('/api/summaries/' + str(self.document.summary.id))
        assert response.status_code == 404
        # 4. user is logged in but not the owner of the question
        response = api_client.get('/api/questions/' + str(self.document.questions[0].id))
        assert response.status_code == 404

        # logout
        api_client.logout()


    def test_document_deletion_cross_user(self):
        # ensure user2 cannot delete user1's document
        self.client.force_login(self.user2)
        response = self.client.delete('/api/documents/' + str(self.document.id))
        assert response.status_code == 404
        self.client.logout()

    # see if the document deletes its associated summary and questions, file, and ocr when deleted
    def test_document_deletion(self):
        # ensure user1 can delete their own document
        self.client.force_login(self.user)
        response = self.client.delete('/api/documents/' + str(self.document.id))
        assert response.status_code == 204
        self.client.logout()
        assert not self.document.summary
        assert not self.document.questions
        assert not self.document.file
        assert not self.document.text

    def tearDown(self):
        self.document.delete()
        self.user.delete()
        self.document2.delete()
        self.user2.delete()

class TestSummary(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create(username='test_user', password='test_password')
        self.document = Document.objects.create(user=self.user, title='test_document', file='test_file.pdf')
        self.document.save()
        # create a new text file
        with open('test_text.txt', 'w', encoding='utf-8') as f:
            f.write('test_content')
        self.summary = Summary.objects.create(document=self.document, content='test_text.txt')
        self.summary.save()
        # delete the text file
        os.remove('test_text.txt')

    def test_summary_creation(self):
        self.assertEqual(self.summary.document, self.document)
        self.assertEqual(self.summary.content, self.text_file)

    def test_summary_get_summary(self):
        self.assertEqual(self.summary.get_summary(), 'test_content')

class TestQuestion(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create(username='test_user', password='test_password')
        self.document = Document.objects.create(user=self.user, title='test_document', file='test_file.pdf')
        self.document.save()
        self.question = Question.objects.create(document=self.document, question='test_question',
                                                answer='test_answer')
        self.question.save()

    def test_question_creation(self):
        self.assertEqual(self.question.document, self.document)
        self.assertEqual(self.question.question, 'test_question')
        self.assertEqual(self.question.answer, 'test_answer')

# assert a user can delete a document and the document/summary/questions are deleted in cascade

"""