# Generated by Django 3.2.7 on 2021-09-07 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0003_auto_20210907_1314'),
    ]

    operations = [
        migrations.AlterField(
            model_name='academic',
            name='level',
            field=models.DecimalField(blank=True, decimal_places=1, max_digits=4, null=True),
        ),
        migrations.AlterField(
            model_name='academic',
            name='subscribers',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=9, null=True),
        ),
    ]
