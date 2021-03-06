# Generated by Django 3.2.7 on 2021-09-11 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0012_alter_article_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='stakers',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=6, null=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='rating',
            field=models.DecimalField(blank=True, decimal_places=1, max_digits=2, null=True),
        ),
    ]
