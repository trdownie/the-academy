# Generated by Django 3.2.6 on 2021-08-26 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0002_remove_academic_subjects'),
        ('articles', '0006_auto_20210825_1921'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='authors',
            field=models.ManyToManyField(to='academics.Academic'),
        ),
    ]
