from django.test import TestCase

from .models import Document, Summary, Question

# use pytest, not hypothesis. that's too complicated for now.

# test that another user cannot access a document that is not theirs

# test that you can delete a document

# for forms, test that all uploaded documents
# have a filetype of pdf, and a title

# test that uploading the dummy pdf activates text extraction

# test that the text extraction task works: ie returns something in ocr_text

# test that summarizing and questions both work.
# for the dummy pdf, you should have 3 questions.

# test uploading profile pictures

