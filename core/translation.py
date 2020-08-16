from modeltranslation.translator import translator, TranslationOptions
from core.models import *


# class EventTypeTranslationOption(TranslationOptions):
#     fields = ('title',)
#
#
# translator.register(EventType, EventTypeTranslationOption)

class SiteSettingsTranslationOption(TranslationOptions):
    fields = (
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


class HowItWorksTranslationOption(TranslationOptions):
    fields = (
        'content',
    )


class MenuTranslationOption(TranslationOptions):
    fields = (
        'title',
    )


translator.register(SiteSettings, SiteSettingsTranslationOption)
translator.register(HowItWorks, HowItWorksTranslationOption)
translator.register(Menu, MenuTranslationOption)
