# Generated by Django 3.2.7 on 2021-09-11 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0013_auto_20210911_1403'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='stakers',
            field=models.DecimalField(blank=True, decimal_places=0, default=0, max_digits=6, null=True),
        ),
    ]