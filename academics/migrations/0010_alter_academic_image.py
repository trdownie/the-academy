# Generated by Django 3.2.7 on 2021-09-16 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0009_alter_academic_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='academic',
            name='image',
            field=models.ImageField(blank=True, default='/noimage.jpeg', upload_to=''),
        ),
    ]
