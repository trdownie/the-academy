# Generated by Django 3.2.7 on 2021-09-02 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='country',
            field=models.CharField(default='placeholder', max_length=40),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='county',
            field=models.CharField(blank=True, max_length=80),
        ),
        migrations.AddField(
            model_name='order',
            name='phone_number',
            field=models.CharField(default='placeholder', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='postcode',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='order',
            name='street_address1',
            field=models.CharField(default='placeholder', max_length=80),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='street_address2',
            field=models.CharField(blank=True, max_length=80),
        ),
        migrations.AddField(
            model_name='order',
            name='town_or_city',
            field=models.CharField(default='placeholder', max_length=40),
            preserve_default=False,
        ),
    ]