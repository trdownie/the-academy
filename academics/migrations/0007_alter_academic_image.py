# Generated by Django 3.2.7 on 2021-09-16 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0006_remove_academic_subscribers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='academic',
            name='image',
            field=models.ImageField(blank=True, default='/media/noimage.jpeg', upload_to=''),
        ),
    ]
