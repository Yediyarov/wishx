# Generated by Django 2.0.1 on 2019-07-29 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_wish_identification_card_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wish',
            name='identification_card_image',
            field=models.ImageField(blank=True, null=True, upload_to='identification_card_image'),
        ),
    ]