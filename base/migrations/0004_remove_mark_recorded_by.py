# Generated by Django 5.0.4 on 2024-04-17 04:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_remove_mark_recorded_by_mark_recorded_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mark',
            name='recorded_by',
        ),
    ]
