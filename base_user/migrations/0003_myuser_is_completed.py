# Generated by Django 2.0.1 on 2019-07-04 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base_user', '0002_auto_20190704_1656'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='is_completed',
            field=models.BooleanField(default=False, verbose_name='completed'),
        ),
    ]