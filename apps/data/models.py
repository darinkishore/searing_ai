from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

import json

from apps.utils.models import BaseModel
from ..users.models import CustomUser
from .storage_backends import PrivateMediaStorage



class Document(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name='documents')
    title = models.CharField(max_length=255, default=None)

    # file that holds the actual document
    file = models.FileField(storage=PrivateMediaStorage,
                            upload_to="documents/", default=None)

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
