# Generated by Django 2.0.1 on 2019-07-17 07:08

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_howitworks'),
    ]

    operations = [
        migrations.AddField(
            model_name='howitworks',
            name='content_az',
            field=ckeditor.fields.RichTextField(null=True),
        ),
        migrations.AddField(
            model_name='howitworks',
            name='content_en',
            field=ckeditor.fields.RichTextField(null=True),
        ),
        migrations.AddField(
            model_name='howitworks',
            name='content_ru',
            field=ckeditor.fields.RichTextField(null=True),
        ),
    ]