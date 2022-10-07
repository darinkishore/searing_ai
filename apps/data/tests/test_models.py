import time

from django.test import TestCase, Client
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse

from ..models import Document, Summary, Question
from ...users.models import CustomUser


class TestDocument(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create(username='test_user', password='test_password')
        self.document = Document.objects.create(user=self.user, title='test_document', file='test_file.pdf')
        self.document.save()

        # second user and second document
        self.user2 = CustomUser.objects.create(username='test_user2', password='test_password2')
        self.document2 = Document.objects.create(user=self.user2, title='test_document2', file='test_file2.pdf')
        self.document2.save()

    # see if a document can be created
    def test_document_creation(self):
        self.assertEqual(self.document.title, 'test_document')
        self.assertEqual(self.document.file, 'test_file.pdf')
        self.assertEqual(self.document.user, self.user)

    # see if the ocr is successfully generated
    def test_document_ocr(self):
        self.document.start_text_extraction()
        while self.document.get_text_extraction() != 'DONE':
            time.sleep(2)
            if self.document.get_text_extraction() == 'FAILED':
                assert False
        self.document.get_text_extraction()
        self.document.extract_text()
        assert self.document.text

    # see if there is a summary generated
    def test_document_summary(self):
        # depends on ocr being done
        if self.document.get_text_extraction() == 'DONE':
            self.document.create_summary()
            assert self.document.summary
            assert self.document.summary.get_summary
        else:
            self.document.start_text_extraction()
            while self.document.get_text_extraction() != 'DONE':
                time.sleep(2)
        self.document.get_text_extraction()
        self.document.extract_text()
        self.document.create_summary()

    # see if there are questions generated
    def test_document_questions(self):
        self.document.create_questions()
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
        assert response.data[0]['title'] == 'test_document'
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
        response = self.client.delete('/api/documents/' + str(self.document.id) +)
        assert response.status_code == 404
        self.client.logout()

    # see if the document deletes its associated summary and questions, file, and ocr when deleted
    def test_document_deletion(self):
        # ensure user1 can delete their own document
        self.client.force_login(self.user)
        response = self.client.delete('/api/documents/' + str(self.document.id) +)
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
            self.text_file = open('test_text.txt', 'w', encoding='utf-8')
            self.text_file.write('test_content')
            self.text_file.close()
            self.summary = Summary.objects.create(document=self.document, content=self.text_file)
            self.summary.save()

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

# assert a user can only access their own documents
# assert a user cannot access another user's documents
# assert a user can delete a document and the document/summary/questions are deleted in cascade
