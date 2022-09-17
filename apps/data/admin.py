from django.contrib import admin

# Register your models here.

from .models import Document, Summary, Question

admin.site.register(Document)
admin.site.register(Summary)
admin.site.register(Question)

