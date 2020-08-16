from django import forms
from django.contrib.auth import get_user_model
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import ReadOnlyPasswordHashField, AuthenticationForm
from django.contrib.auth import authenticate
from base_user.tools.common import GENDER

from PIL import Image

# get custom user
User = get_user_model()


class MyUserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': _('E-poçt'), 'class': 'form-input mb-5'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': _('Şifrə'), 'class': 'form-input', 'id': 'sign-up-password'}))

    remember_me = forms.BooleanField(required=False,
        widget=forms.CheckboxInput(attrs={'class': 'option-input checkbox small'}))

    def clean_username(self):
        username = self.cleaned_data.get("username")
        user = User.objects.filter(username__iexact=username).first()
        if user:
            return user.email
        return username.lower()

    error_messages = {
        'invalid_login': _('You have entered an invalid email or password'),
    }


class MyUserCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given email and
    password.
    """
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    password1 = forms.CharField(label=_("Password"),
        widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"),
        widget=forms.PasswordInput,
        help_text=_("Enter the same password as above, for verification."))

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name")

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(MyUserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class MyUserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(label=_("Password"),
        help_text=_(
            "Raw şifrələr bazada saxlanmır, onları heç cürə görmək mümkün deyil "
            "bu istifadəçinin şifrəsidir, lakin siz onu dəyişə bilərsiziniz "
            " <a href=\"../password/\">bu form</a>. vasitəsilə"))

    class Meta:
        model = User
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(MyUserChangeForm, self).__init__(*args, **kwargs)
        f = self.fields.get('user_permissions', None)
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class BaseRegistrationForm(forms.ModelForm):
    """
        A form that creates a user, with no privileges, from the given email and
        password.
        """
    error_messages = {
        'password_incorrect': _("Cari şifrə yanlışdır"),
    }
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': _("Şifrə"), 'id': 'sign-up-password', 'class': 'form-input'}))
    gender = forms.ChoiceField(choices=GENDER, widget=forms.RadioSelect(attrs={'class': 'option-input radio mr-1'}),
        required=True)

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'gender',
        )
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': _('Ad'), 'class': 'form-input mb-5'}),
            'last_name': forms.TextInput(attrs={'placeholder': _('Soyad'), 'class': 'form-input mb-5'}),
            'email': forms.EmailInput(attrs={'placeholder': _('Email'), 'class': 'form-input mb-5'}),
        }
        custom_error_messages = {
            'required': _("This field is required"),
            'invalid': _('Invalid value for this field'),
        }
        error_messages = {
            'email': {
                'required': _("This field is required"),
                'invalid': _('Invalid value for this field'),
                'unique': _('This email is already registered'),
            },
            'first_name': custom_error_messages,
            'last_name': custom_error_messages,
            'gender': custom_error_messages,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        required_fields = (
            'first_name',
            'last_name',
            'email',
        )
        for field in required_fields:
            if field in self.fields and not self.fields[field].required:
                self.fields[field].required = True

    def clean_email(self):
        email = self.cleaned_data.get("email")
        return email.lower()

    def clean_first_name(self):
        isascii = lambda s: len(s) == len(s.encode())
        if not isascii(self.cleaned_data['first_name']):
            raise forms.ValidationError(
                _("Yalnız ingilis hərfləri")
            )
        return self.cleaned_data['first_name']

    def clean_last_name(self):
        isascii = lambda s: len(s) == len(s.encode())
        if not isascii(self.cleaned_data['last_name']):
            raise forms.ValidationError(
                _("Yalnız ingilis hərfləri")
            )

        return self.cleaned_data['last_name']

    def save(self, commit=True):
        user = super(BaseRegistrationForm, self).save(commit=False)
        user.username = user.email
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class AccountEditForm(forms.ModelForm):
    gender = forms.ChoiceField(choices=GENDER, widget=forms.RadioSelect(attrs={'class': 'option-input radio mr-1'}),
        required=True)

    # day = forms.ChoiceField(choices=DAYS, required=True)

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'gender',
            'profile_picture',
        )
        widgets = {
            'first_name': forms.TextInput(
                attrs={'placeholder': _('Ad'), 'class': 'form-input w-100', 'id': 'person-name'}),
            'last_name': forms.TextInput(
                attrs={'placeholder': _('Soyad'), 'class': 'form-input w-100', 'id': 'person-surname'}),
            'email': forms.EmailInput(
                attrs={'placeholder': _('Email'), 'class': 'form-input w-100', 'id': 'person-email'}),
            'profile_picture': forms.FileInput(
                attrs={'class': 'd-none', 'id': 'profile-photo-input', 'accept': 'image/jpeg, image/png'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.get('user')
        kwargs.pop('user')
        super().__init__(*args, **kwargs)
        required_fields = (
            'first_name',
            'last_name',
            'email',
        )
        for field in required_fields:
            if field in self.fields and not self.fields[field].required:
                self.fields[field].required = True

    def clean_first_name(self):
        isascii = lambda s: len(s) == len(s.encode())
        if not isascii(self.cleaned_data['first_name']):
            raise forms.ValidationError(
                _("Yalnız ingilis hərfləri")
            )
        return self.cleaned_data['first_name']

    def clean_last_name(self):
        isascii = lambda s: len(s) == len(s.encode())
        if not isascii(self.cleaned_data['last_name']):
            raise forms.ValidationError(
                _("Yalnız ingilis hərfləri")
            )

        return self.cleaned_data['last_name']

    def save(self, commit=True):
        user = super(AccountEditForm, self).save(commit=False)
        user.username = user.email
        if commit:
            user.save()
        return user


class AccountUpdateForm(AccountEditForm, BaseRegistrationForm):
    old_password = forms.CharField(required=False, label=_("Hazırki Şifrə"),
        widget=forms.PasswordInput(
            attrs={'class': 'form-input w-100', 'id': 'person-old-password', 'placeholder': _('Köhnə şifrə')}))

    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'placeholder': _("Yeni şifrə"), 'id': 'person-new-password', 'class': 'form-input w-100'}))

    def __init__(self, *args, **kwargs):
        self.user = kwargs.get('user')
        super().__init__(*args, **kwargs)

        self.fields['password1'].required = False
        self.fields['password1'].label = _("Yeni Şifrə")

    def save(self, commit=True):
        if self.cleaned_data["password1"]:
            self.user.set_password(self.cleaned_data["password1"])
        self.instance.save()
        self._save_m2m()
        return self.instance

    def clean_old_password(self):
        """
        Validate that the old_password field is correct.
        """
        password1 = self.cleaned_data.get("password1")
        old_password = self.cleaned_data["old_password"]
        if old_password or password1:
            if not self.user.check_password(old_password):
                raise forms.ValidationError(
                    self.error_messages['password_incorrect'],
                    code='password_incorrect',
                )

        return old_password
