# Generated by Django 3.1 on 2020-09-01 17:31

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0005_auto_20200901_1707'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place',
            name='description_long',
            field=tinymce.models.HTMLField(),
        ),
    ]