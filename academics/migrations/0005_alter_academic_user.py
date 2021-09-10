# Generated by Django 3.2.7 on 2021-09-10 17:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('academics', '0004_auto_20210907_1345'),
    ]

    operations = [
        migrations.AlterField(
            model_name='academic',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='academic', to=settings.AUTH_USER_MODEL),
        ),
    ]
