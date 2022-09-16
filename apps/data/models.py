from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from apps.utils.models import BaseModel
from ..users.models import CustomUser
from .storage_backends import PrivateMediaStorage


# TODO: add validation for file size, type


class Document(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name='documents')
    title = models.CharField(max_length=255, default=None)

    # file that holds the actual document
    file = models.FileField(storage=PrivateMediaStorage,
                            upload_to="documents/", default=None,)

    # summary, questions are one-one field with document


class Summary(BaseModel):
    document = models.OneToOneField("Document", on_delete=models.CASCADE, related_name="summary",
                                    null=True, default=None)
    content = models.TextField(null=True, default=None)

    @property
    def summary(self):
        return self.content

    @summary.setter
    def summary(self, value):
        self.content = value

    def __str__(self):
        return f"Summary of {self.document.title}"


class Questions(BaseModel):
    document = models.OneToOneField("Document", on_delete=models.CASCADE, related_name="questions",
                                    null=True, default=None)
    # delimited string, split by question mark
    questions = models.TextField()

    def __str__(self):
        return f"Question of {self.document.title}"

    @property
    def get_questions(self):
        return self.questions.split("?")

    def num_questions(self):
        return len(self.get_questions)

    def get_question(self, index):
        return self.get_questions[index]