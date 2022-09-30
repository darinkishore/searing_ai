# Generated by Django 4.1.1 on 2022-09-20 04:33

import apps.data.storage_backends
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0007_document_job_id_document_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='ocr_text',
            field=models.FileField(blank=True, default=None, null=True, storage=apps.data.storage_backends.PrivateMediaStorage, upload_to='documents/'),
        ),
        migrations.AlterField(
            model_name='document',
            name='job_id',
            field=models.CharField(blank=True, default=None, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='document',
            name='text',
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
    ]