# Generated by Django 4.1.1 on 2022-09-23 00:16

import annoying.fields
from django.db import migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0009_alter_summary_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='summary',
            name='document',
            field=annoying.fields.AutoOneToOneField(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='summary', to='data.document'),
        ),
    ]
