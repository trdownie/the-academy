# Generated by Django 3.2.6 on 2021-08-25 11:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0004_rename_subject_subject_subject_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='subject',
            options={'ordering': ['subject_name']},
        ),
    ]