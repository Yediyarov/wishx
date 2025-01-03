# Generated by Django 2.0.1 on 2019-07-17 07:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_auto_20190717_1108'),
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('title_az', models.CharField(blank=True, max_length=255, null=True)),
                ('title_ru', models.CharField(blank=True, max_length=255, null=True)),
                ('title_en', models.CharField(blank=True, max_length=255, null=True)),
                ('url', models.CharField(blank=True, max_length=255, null=True)),
                ('base', models.BooleanField(default=True)),
                ('order', models.IntegerField()),
                ('status', models.BooleanField(default=True)),
                ('sub_menu', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='submenus', to='core.Menu')),
            ],
            options={
                'verbose_name': 'Main page menus',
                'verbose_name_plural': 'Main page menus',
                'ordering': ('order',),
            },
        ),
    ]
