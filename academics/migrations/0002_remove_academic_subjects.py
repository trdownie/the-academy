# Generated by Django 3.2.6 on 2021-08-26 10:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='academic',
            name='subjects',
        ),
    ]
