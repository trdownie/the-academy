# Generated by Django 3.2.6 on 2021-08-23 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0002_auto_20210823_1127'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='image',
            field=models.ImageField(blank=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='article',
            name='image_url',
            field=models.URLField(blank=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6),
        ),
        migrations.AlterField(
            model_name='article',
            name='rating',
            field=models.DecimalField(blank=True, decimal_places=1, max_digits=5),
        ),
    ]
