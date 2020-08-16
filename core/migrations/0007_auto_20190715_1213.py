# Generated by Django 2.0.1 on 2019-07-15 08:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_privacypolicy'),
    ]

    operations = [
        migrations.AddField(
            model_name='like',
            name='reply',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='core.Reply'),
        ),
        migrations.AlterField(
            model_name='like',
            name='donation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='core.Donation'),
        ),
    ]