import time

from django.core.files.base import ContentFile
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _



import boto3
import environ
import string

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
                'SNSTopicArn': 'arn:aws:sns:us-east-1:361149468120:TextractSNSTopic',
                'RoleArn': 'arn:aws:iam::361149468120:role/text'})
        self.job_id = job_id['JobId']
        self.save()


    def get_text_extraction(self):
        # polls the SNS topic for the job id
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
        for block in blocks:
            if block['BlockType'] == 'PAGE':
                pages.append(block['Page'])

        # TODO: add processing by line location

        for page in pages:
            page_text = ''
            for block in blocks:
                if block['BlockType'] == 'LINE' and block['Page'] == page:
                    page_text.append(block['Text'], encoding='utf-8')
                    page_text.append(' ', encoding='utf-8')
                    page_text.append('\n', encoding='utf-8')
            doc_text.append(page_text, encoding='utf-8')

        # create text file of content and save to s3
        doc_text = doc_text.encode()
        with open(f'{self.title}_summary.txt', 'wb') as f:
            f.write(doc_text)
        self.ocr_text = f'{self.title}_summary.txt'
        self.save()


# summary, questions are one-one field with document

class Summary(BaseModel):
    document = models.OneToOneField("Document", on_delete=models.CASCADE, related_name="summary",
                                    null=True, default=None)
    content = models.TextField(default=None)

    @property
    def get_summary(self):
        return self.content

    # set summary
    def set_summary(self, summary):
        self.content = summary
        self.save()

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
