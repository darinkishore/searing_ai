import os

from django.core.files.base import ContentFile
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

import boto3

import openai
from annoying.fields import AutoOneToOneField

from apps.utils.models import BaseModel
from ..users.models import CustomUser
from .storage_backends import PrivateMediaStorage

AWS_ACCESS_KEY_ID = os.environ.get('TEXTRACT_CRED')
AWS_SECRET_ACCESS_KEY = os.environ.get('TEXTRACT_PASS')
AWS_REGION = os.environ.get('AWS_REGION')


class Document(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name='documents')
    title = models.CharField(max_length=255, default=None)

    # file that holds the actual document
    file = models.FileField(storage=PrivateMediaStorage,
                            upload_to="documents/", default=None)

    text = models.JSONField(default=dict, blank=True, null=True)
    job_id = models.CharField(max_length=255, default=None, null=True, blank=True)

    ocr_text = models.TextField(default=None, null=True, blank=True)

    def is_processed(self):
        return self.job_id

    # convert created_at from GMT to local time
    def get_created_at(self):
        return self.created_at.astimezone()

    def __str__(self):
        return f'{self.title}'

    def clean(self):
        # check if the file is a pdf
        if not self.file.name.endswith('.pdf'):
            raise ValidationError(_('File must be a PDF'))

        # check if the file is less than 5mb
        if self.file.size > 5242880:
            raise ValidationError(_('File must be less than 5mb'))

        # check if the file is empty
        if self.file.size == 0:
            raise ValidationError(_('File cannot be empty'))

        # check if the file is a duplicate
        if Document.objects.filter(file=self.file).exists():
            raise ValidationError(_('File already exists'))

        # trim whitespace from title
        self.title = self.title.strip()

    def start_text_extraction(self):
        # make a boto3 s3 client to get the file from a user's private s3 bucket
        # start text extraction job
        textract = boto3.client('textract', aws_access_key_id=AWS_ACCESS_KEY_ID,
                                aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                                region_name=AWS_REGION)

        name = 'private/' + self.file.name
        # make a boto3 s3 client to get the file from a user's private s3 bucket

        job_id = textract.start_document_text_detection(
            DocumentLocation={
                'S3Object': {
                    'Bucket': 'moshimedia',
                    'Name': name
                }
            })
        self.job_id = job_id['JobId']
        self.save()

    def get_text_extraction(self):
        # if the job is complete, it will return the text
        # if the job is not complete, it will return None
        # if the job is already done, it will return the text
        if self.job_id == 'PROCESSED':
            return self.text

        textract = boto3.client('textract', aws_access_key_id=AWS_ACCESS_KEY_ID,
                                aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                                region_name=AWS_REGION)

        response = textract.get_document_text_detection(JobId=self.job_id)

        if response['JobStatus'] == 'IN_PROGRESS':
            return None
        elif response['JobStatus'] == 'FAILED':
            return 'FAILED'
        elif response['JobStatus'] == 'SUCCEEDED':
            self.job_id = 'PROCESSED'
            self.text = response
            self.save()
            return 'DONE'

    def extract_text(self):
        # iteratively builds a string of the entire document
        text = self.text
        blocks = text['Blocks']
        pages = []
        doc_text = ''
        doc_text.encode('utf-8')
        for block in blocks:
            if block['BlockType'] == 'PAGE':
                pages.append(block['Page'])

        # TODO: add processing by line location

        for page in range(1, max(pages) + 1):
            page_text = ''
            for block in blocks:
                if block['BlockType'] == 'LINE':
                    page_text += block['Text'] + ' ' + '\n'
            doc_text += page_text + '\n'

        # save the file to the ocr_text field
        self.ocr_text = doc_text
        self.save()

    def create_summary(self):
        """
        create a summary of the document
        """
        openai.api_key = os.environ.get('OPENAI_KEY')
        text_to_summarize = self.ocr_text

        text_to_summarize = text_to_summarize.split('.')
        # list of sentence strings
        broken_text = []

        block = []
        block_size = 0
        for sentence in text_to_summarize:  # string
            # count characters in sentence
            if block_size + len(sentence) < 12000:  # should be approximately within token length
                block.append(sentence)
                block_size += len(sentence)
            # if the block is too long, append it to the broken text list and reset the block
            elif block_size + len(sentence) >= 12000:
                broken_text.append(block)
                block = []
            # if the sentence is the last sentence in the document
            if sentence == text_to_summarize[-1]:
                broken_text.append(block)

        summary = ''
        for block in broken_text:
            block_content = ' '.join(block).strip()
            response = openai.Completion.create(
                model="text-davinci-002",
                prompt=f'Summarize the given text for a university student.'
                       f'Give them the most important information to '
                       f'learn the content of this text.\n'
                       f'Given text: \n {block_content} <|endoftext|>',
                max_tokens=400,
                temperature=0.3,
                presence_penalty=-0.75,
            )
            # basically how you get the summary for each block
            summary += response['choices'][0]['text'] + '\n'

        self.summary.content = summary
        self.summary.save()

    def create_questions(self):
        """
        generate questions for the document
        """
        openai.api_key = os.environ.get('OPENAI_KEY')
        text_to_generate_questions = self.summary.get_summary

        num_questions = len(text_to_generate_questions) / 100
        if num_questions <= 1:
            num_questions = 3

        response = openai.Completion.create(
            model="text-davinci-002",
            prompt=f'Given this text, generate {num_questions} questions to test'
                   f'understanding of the text. The questions should'
                   f'be at the level of a university student, and test'
                   f'recall of the content, background information, and application of the content'
                   f'to other mediums. They should not be easy, unless they test recall.\n'
                   f'At least one of the questions should relate to an application of the content. \n'
                   f'Examples:\n'
                   f'Q: What is the main idea of this text?\n'
                   f'A: The author argues for institutional reform to improve the lives of the poor.\n'
                   f'Q: What does the term \"institutional reform\" mean?\n'
                   f'A: Institutional reform is a change in the way that a society is organized.\n'
                   f'Q: Why would institutional reform be necessary, according to the author?\n'
                   f'A: The author argues that the rich owe a moral debt to humanity.\n'
                   f'Q: What would institutional reform create? (The answer to this is not provided by the document)\n'
                   f'A: A more just society.\n'
                   f'Given text: \n {text_to_generate_questions}'
                   f'<|endoftext|>',
            max_tokens=400,
            temperature=0.7,
            presence_penalty=.15,
        )

        questions = response['choices'][0]['text']
        # questions will be in Q: \n A: \n format.
        # get question answer pairs, generated from paired Q: and A: prompts.
        question_pair = questions.split('Q: ')
        question_answer_pairs = []
        for pair in question_pair:
            if pair != '' or pair != '\n\n':
                question_answer_pairs.append(pair.split('A: '))

        # create question object for each pair
        for pair in question_answer_pairs:
            if len(pair) == 2:
                question = pair[0].strip()
                answer = pair[1].strip()
                Question.objects.create(
                    question=question,
                    answer=answer,
                    document=self
                )


# summary, questions are one-one field with document

class Summary(BaseModel):
    document = AutoOneToOneField("Document", on_delete=models.CASCADE, related_name="summary",
                                 default=None, primary_key=True)
    content = models.TextField(null=True, blank=True, default=None)

    @property
    def get_summary(self):
        return self.content

    def __str__(self):
        return f"Summary of {self.document.title}"


class Question(BaseModel):
    document = models.ForeignKey("Document", on_delete=models.CASCADE, related_name="questions",
                                 default=None)

    # delimited string, split by question mark
    question = models.TextField(default=None)
    answer = models.TextField(default=None)

    def __str__(self):
        return f"Question of {self.document.title}"
