from django.contrib import admin
from core.models import *


# Register your models here.

class ImageStackedInline(admin.TabularInline):
    model = Image
    extra = 0
    readonly_fields = ('preview_image',)
    fields = ('url', 'preview_image', 'order',)
    classes = ('collapse',)


@admin.register(EventType)
class EventTypeAdmin(admin.ModelAdmin):
    list_display = ('title',)


@admin.register(Wish)
class WishAdmin(admin.ModelAdmin):
    inlines = [ImageStackedInline]
    readonly_fields = ('slug', 'event_type_title',)
    search_fields = (
        'name',
        'surname',
        'title',
        'description',
    )
    list_display = (
        'name',
        'surname',
        'title',
        'accumulated_amount',
        'number_of_donations',
        'deadline',
        'created_at',
        'is_deleted',
    )
    list_filter = (
        'currency',
        'number_of_donations',
        'accumulated_amount',
        'published',
    )
    # save_as = True


@admin.register(AmountRange)
class AmountRangeAdmin(admin.ModelAdmin):
    list_display = ('event_type',)


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ('user', 'wish', 'comment', 'amount', 'currency', 'created_at',)
    list_filter = ('user', 'wish',)


@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ('user', 'comment', 'donation', 'created_at',)
    search_fields = ('comment',)
    list_filter = ('user', 'donation',)
    readonly_fields = ('user', 'donation',)


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'donation', 'reply', 'created_at',)
    list_filter = ('user', 'donation', 'reply',)


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    exclude = (
        'main_page_first_section_title',
        'main_page_first_section_text',
        'main_page_second_section_title',
        'main_page_second_section_text',
        'main_page_third_section_title',
        'main_page_third_section_text',
        'main_page_fourth_section_title',
        'main_page_fourth_section_text',
        'footer_sign_up_title',
        'footer_copyright_text',
    )


@admin.register(PrivacyPolicy)
class PrivacyPolicyAdmin(admin.ModelAdmin):
    list_display = ('content',)


@admin.register(Subscribers)
class SubscribersAdmin(admin.ModelAdmin):
    list_display = ('email',)


@admin.register(HowItWorks)
class HowItWorksAdmin(admin.ModelAdmin):
    exclude = ('content',)


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    exclude = ('title',)
    list_display = ('title', 'status', 'base', 'order',)
