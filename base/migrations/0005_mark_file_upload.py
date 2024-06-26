# Generated by Django 5.0.4 on 2024-04-17 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_remove_mark_recorded_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='mark',
            name='file_upload',
            field=models.FileField(help_text='Upload file with student marks.', null=True, upload_to='uploads/%Y/%m/%d/'),
        ),
    ]
