# Generated by Django 2.0.1 on 2019-07-11 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20190706_1513'),
    ]

    operations = [
        migrations.AddField(
            model_name='reply',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]