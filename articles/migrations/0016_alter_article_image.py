# Generated by Django 3.2.7 on 2021-09-16 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0015_alter_article_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='image',
            field=models.ImageField(blank=True, default='https://s3.console.aws.amazon.com/s3/object/the-home-of-learning?region=eu-west-2&prefix=media/noimage.jpeg', upload_to=''),
        ),
    ]