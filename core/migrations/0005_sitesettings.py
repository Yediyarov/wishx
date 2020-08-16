# Generated by Django 2.0.1 on 2019-07-13 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_reply_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('main_page_first_section_title', models.CharField(blank=True, max_length=255, null=True)),
                ('main_page_first_section_title_az', models.CharField(blank=True, max_length=255, null=True)),
                ('main_page_first_section_title_ru', models.CharField(blank=True, max_length=255, null=True)),
                ('main_page_first_section_title_en', models.CharField(blank=True, max_length=255, null=True)),
                ('main_page_first_section_text', models.TextField(blank=True, null=True)),
                ('main_page_first_section_text_az', models.TextField(blank=True, null=True)),
                ('main_page_first_section_text_ru', models.TextField(blank=True, null=True)),
                ('main_page_first_section_text_en', models.TextField(blank=True, null=True)),
                ('main_page_second_section_title', models.CharField(blank=True, max_length=255, null=True)),
                ('main_page_second_section_title_az', models.CharField(blank=True, max_length=255, null=True)),
                ('main_page_second_section_title_ru', models.CharField(blank=True, max_length=255, null=True)),
                ('main_page_second_section_title_en', models.CharField(blank=True, max_length=255, null=True)),
                ('main_page_second_section_text', models.TextField(blank=True, null=True)),
                ('main_page_second_section_text_az', models.TextField(blank=True, null=True)),
                ('main_page_second_section_text_ru', models.TextField(blank=True, null=True)),
                ('main_page_second_section_text_en', models.TextField(blank=True, null=True)),
                ('main_page_third_section_title', models.CharField(blank=True, max_length=255, null=True)),
                ('main_page_third_section_title_az', models.CharField(blank=True, max_length=255, null=True)),
                ('main_page_third_section_title_ru', models.CharField(blank=True, max_length=255, null=True)),
                ('main_page_third_section_title_en', models.CharField(blank=True, max_length=255, null=True)),
                ('main_page_third_section_text', models.TextField(blank=True, null=True)),
                ('main_page_third_section_text_az', models.TextField(blank=True, null=True)),
                ('main_page_third_section_text_ru', models.TextField(blank=True, null=True)),
                ('main_page_third_section_text_en', models.TextField(blank=True, null=True)),
                ('main_page_fourth_section_title', models.CharField(blank=True, max_length=255, null=True)),
                ('main_page_fourth_section_title_az', models.CharField(blank=True, max_length=255, null=True)),
                ('main_page_fourth_section_title_ru', models.CharField(blank=True, max_length=255, null=True)),
                ('main_page_fourth_section_title_en', models.CharField(blank=True, max_length=255, null=True)),
                ('main_page_fourth_section_text', models.TextField(blank=True, null=True)),
                ('main_page_fourth_section_text_az', models.TextField(blank=True, null=True)),
                ('main_page_fourth_section_text_ru', models.TextField(blank=True, null=True)),
                ('main_page_fourth_section_text_en', models.TextField(blank=True, null=True)),
                ('footer_sign_up_title', models.CharField(blank=True, max_length=255, null=True)),
                ('footer_sign_up_title_az', models.CharField(blank=True, max_length=255, null=True)),
                ('footer_sign_up_title_ru', models.CharField(blank=True, max_length=255, null=True)),
                ('footer_sign_up_title_en', models.CharField(blank=True, max_length=255, null=True)),
                ('footer_copyright_text', models.CharField(blank=True, max_length=255, null=True)),
                ('footer_copyright_text_az', models.CharField(blank=True, max_length=255, null=True)),
                ('footer_copyright_text_ru', models.CharField(blank=True, max_length=255, null=True)),
                ('footer_copyright_text_en', models.CharField(blank=True, max_length=255, null=True)),
                ('footer_contact_email', models.CharField(blank=True, max_length=255, null=True)),
                ('footer_contact_number', models.CharField(blank=True, max_length=255, null=True)),
                ('twitter_profile_url', models.URLField(blank=True, verbose_name='twitter_hyperlink')),
                ('instagram_profile_url', models.URLField(blank=True, verbose_name='instagram_hyperlink')),
                ('facebook_profile_url', models.URLField(blank=True, verbose_name='facebook_hyperlink')),
                ('youtube_profile_url', models.URLField(blank=True, verbose_name='youtube_hyperlink')),
            ],
            options={
                'verbose_name': 'Site setting',
                'verbose_name_plural': 'Site settings',
            },
        ),
    ]