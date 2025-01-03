# Generated by Django 2.0.1 on 2019-07-17 07:04

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20190716_1919'),
    ]

    operations = [
        migrations.CreateModel(
            name='HowItWorks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', ckeditor.fields.RichTextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'How It Works',
                'verbose_name_plural': 'How It Works',
            },
        ),
    ]
