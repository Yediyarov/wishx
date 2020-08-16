from django import template
from core.forms import DonationCommentForm, SubscribeForm
from core.models import SiteSettings, Like, HowItWorks, Menu
from datetime import date

register = template.Library()


@register.simple_tag
def get_comment_form():
    return DonationCommentForm()


@register.simple_tag
def get_subscribe_form():
    return SubscribeForm()


@register.simple_tag
def get_howitworks_content():
    return HowItWorks.objects.last()


@register.simple_tag
def get_menus():
    return Menu.objects.filter(status=True)


@register.simple_tag
def is_liked(donation_id, user_id):
    like = Like.objects.filter(donation_id=donation_id, user_id=user_id).first()
    if like:
        return True
    else:
        return False


@register.simple_tag
def is_liked_comment(comment_id, user_id):
    like = Like.objects.filter(reply_id=comment_id, user_id=user_id).first()
    if like:
        return True
    else:
        return False


@register.simple_tag
def get_site_settings():
    return SiteSettings.objects.last()


@register.simple_tag
def can_create_wish(user):
    date_of_birth = user.date_of_birth
    today = date.today()
    day = date_of_birth.day
    month = date_of_birth.month
    if month == 2 and day == 29:
        day = 28

    birthday = date(today.year, month, day)
    days_until_birthday = (birthday - today).days
    if 60 > days_until_birthday > 0:
        return True
    else:
        return False
