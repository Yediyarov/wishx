# Generated by Django 2.0.1 on 2019-06-28 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eventtype',
            name='title_az',
        ),
        migrations.RemoveField(
            model_name='eventtype',
            name='title_en',
        ),
        migrations.RemoveField(
            model_name='eventtype',
            name='title_ru',
        ),
        migrations.AlterField(
            model_name='eventtype',
            name='title',
            field=models.IntegerField(choices=[(0, 'Ad günü')], default=0, verbose_name='event title'),
        ),
    ]
