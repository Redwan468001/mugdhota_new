# Generated by Django 5.1.3 on 2025-01-06 11:27

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MedicalInsight', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicalscience',
            name='content',
            field=ckeditor.fields.RichTextField(),
        ),
    ]
