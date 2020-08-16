from django import forms
from core.models import *
from django.utils.translation import ugettext_lazy as _
from core.options.tools import CURRENCY


# Your forms here

class WishCreationForm(forms.ModelForm):
    """
    Form for creation wish
    """
    multi_image = forms.FileField(required=False,
        widget=forms.ClearableFileInput(
            attrs={'class': 'd-none',
                   'multiple': True,
                   'accept': 'image/jpeg, image/png',
                   'id': 'event-photo-input',
                   }
        )
    )
    currency = forms.ChoiceField(
        choices=CURRENCY,
        widget=forms.RadioSelect(attrs={'class': 'option-input radio mr-1'}),
        required=True)

    class Meta:
        model = Wish
        fields = (
            'name',
            'surname',
            'title',
            'description',
            'image',
            'required_amount',
            'currency',
            'video',
            # 'published',
            'slug',
            'identification_card_image',
        )

        widgets = {
            'image': forms.FileInput(
                attrs={'class': 'd-none',
                       'id': 'person-photo-input',
                       'accept': 'image/jpeg, image/png'}
            ),
            'identification_card_image': forms.FileInput(
                attrs={'class': 'd-none',
                       'accept': 'image/jpeg, image/png',
                       'id': 'identification-card-input',
                       }
            ),
            'name': forms.TextInput(
                attrs={'class': 'form-input w-100',
                       'id': 'person-name',
                       'placeholder': _('Ad')}
            ),
            'surname': forms.TextInput(
                attrs={'class': 'form-input w-100',
                       'id': 'person-surname',
                       'placeholder': _('Soyad')}
            ),
            'title': forms.TextInput(
                attrs={'class': 'form-input w-100',
                       'id': 'event-name',
                       'placeholder': _('Tədbirin adı')}
            ),
            'slug': forms.TextInput(
                attrs={'class': 'form-input w-100',
                       'id': 'event-shorname',
                       'placeholder': _('Məsələn: menimarzum')}
            ),
            'description': forms.Textarea(
                attrs={'class': 'form-input w-100 textarea pt-4',
                       'id': 'event-desc',
                       'rows': '12'}
            ),
            'required_amount': forms.NumberInput(
                attrs={'class': 'form-input col-7 mr-auto',
                       'id': 'required-amount',
                       'min': '0'}
            ),
            'video': forms.TextInput(
                attrs={'class': 'form-input w-100',
                       'id': 'event-video-input',
                       'placeholder': _('Video yüklə')}
            )
        }

        error_messages = {
            'slug': {
                'unique': _('This short link is already exists')
            },
            'identification_card_image': {
                'required': _('No file selected')
            }
        }


class WishUpdateForm(WishCreationForm):
    pass


class DonationCommentForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = (
            'comment',
        )
        widgets = {
            'comment': forms.Textarea(
                attrs={'class': 'reply__text p-2 px-sm-3 px-md-4 mr-2',
                       'id': 'reply-text',
                       'placeholder': _('Write a reply...'),
                       'rows': '2'
                       }
            ),
        }


class SubscribeForm(forms.ModelForm):
    class Meta:
        model = Subscribers
        fields = ("email",)
        widgets = {
            'email': forms.EmailInput(
                attrs={'class': 'subscribe__input'})
        }
        error_messages = {
            'email': {
                'unique': _('This email is already subscribed')
            }
        }
