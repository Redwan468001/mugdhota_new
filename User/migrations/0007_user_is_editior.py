# Generated by Django 4.2.17 on 2025-02-16 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0006_alter_user_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_editior',
            field=models.BooleanField(default=False),
        ),
    ]
