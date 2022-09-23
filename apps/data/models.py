from django.core.files.base import ContentFile
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

import boto3
import environ
import openai
from annoying.fields import AutoOneToOneField


from apps.utils.models import BaseModel
from ..users.models import CustomUser
from .storage_backends import PrivateMediaStorage

env = environ.Env()
environ.Env.read_env()
AWS_ACCESS_KEY_ID = env('TEXTRACT_CRED')
AWS_SECRET_ACCESS_KEY = env('TEXTRACT_PASS')
AWS_REGION = env('AWS_REGION')


class Document(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name='documents')
    title = models.CharField(max_length=255, default=None)

    # file that holds the actual document
    file = models.FileField(storage=PrivateMediaStorage,
                            upload_to="documents/", default=None)

    text = models.JSONField(default=dict, blank=True, null=True)
    job_id = models.CharField(max_length=255, default=None, null=True, blank=True)

    ocr_text = models.FileField(storage=PrivateMediaStorage,
                                upload_to="documents/", default=None, blank=True, null=True)

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
            },
            NotificationChannel={
                'SNSTopicArn': env('SNS_TOPIC_ARN'),
                'RoleArn': env('SNS_ROLE_ARN')})
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

        # create text file of content and save to s3
        doc_text = doc_text.encode()
        with open(f'{self.title}_text.txt', 'wb') as f:
            f.write(doc_text)
        self.ocr_text.save(f'{self.title}_text.txt', ContentFile(doc_text))

    def create_summary(self):
        """
        create a summary of the document
        """
        openai.api_key = env('OPENAI_KEY')
        text_to_summarize = self.ocr_text.read().decode('utf-8')

        text_to_summarize = text_to_summarize.split('.')
        # list of sentence strings
        broken_text = []
        block = []
        for sentence in text_to_summarize:  # string
            # count characters in sentence
            sent_len = len(sentence)
            if len(block) + sent_len < 13000:  # should be approximately within token length
                block.append(sentence)
            # if the block is too long, append it to the broken text list
            elif len(block) + sent_len >= 13000:
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
            summary += response['choices'][0]['text'] + '\n'

        summary = summary.encode()
        with open(f'{self.title}_summary.txt', 'wb') as f:
            f.write(summary)

        self.summary.content.save(f'{self.title}_summary.txt', ContentFile(summary))

    def generate_questions(self):
        pass



# summary, questions are one-one field with document

class Summary(BaseModel):
    document = AutoOneToOneField("Document", on_delete=models.CASCADE, related_name="summary",
                                    null=True, default=None)
    content = models.FileField(storage=PrivateMediaStorage,
                               upload_to="documents/", default=None, blank=True, null=True)

    @property
    def get_summary(self):
        return self.content.read().decode('utf-8')

    def __str__(self):
        return f"Summary of {self.document.title}"


class Question(BaseModel):
    document = models.ForeignKey("Document", on_delete=models.CASCADE, related_name="questions",
                                 null=True, default=None)

    # delimited string, split by question mark
    question = models.TextField(default=None)
    answer = models.TextField(default=None)

    def __str__(self):
        return f"Question of {self.document.title}"
