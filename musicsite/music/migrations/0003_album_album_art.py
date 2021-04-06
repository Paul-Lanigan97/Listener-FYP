# Generated by Django 3.1.3 on 2021-03-19 17:50

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0002_auto_20210318_0345'),
    ]

    operations = [
        migrations.AddField(
            model_name='album',
            name='album_art',
            field=models.ImageField(blank=True, upload_to='images', validators=[django.core.validators.FileExtensionValidator(['png', 'jpg', 'jpeg'])]),
        ),
    ]
