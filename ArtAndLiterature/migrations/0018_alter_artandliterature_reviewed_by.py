# Generated by Django 4.2.17 on 2025-02-17 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ArtAndLiterature', '0017_rename_revised_by_artandliterature_reviewed_by_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artandliterature',
            name='reviewed_by',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
