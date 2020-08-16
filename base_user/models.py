from django.core.mail import send_mail
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.conf import settings
from django.core import validators
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from base_user.tools.common import get_user_profile_photo_file_name, slugify

USER_MODEL = settings.AUTH_USER_MODEL


class MyUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


# Customize User model
class MyUser(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    First name, last name, date of birth and email are required. Other fields are optional.
    """

    username = models.CharField(_('username'), max_length=100, unique=True,
        help_text=_('Tələb olunur. 75 simvol və ya az. Hərflər, Rəqəmlər və '
                    '@/./+/-/_ simvollar.'),
        validators=[
            validators.RegexValidator(r'^[\w.@+-]+$', _('Düzgün istifadəçi adı daxil edin.'),
                'yanlışdır')
        ], blank=True)
    first_name = models.CharField(_('first name'), max_length=255)
    last_name = models.CharField(_('last name'), max_length=255)
    email = models.EmailField(_('email address'), max_length=255, unique=True, db_index=True)
    profile_picture = models.ImageField(upload_to=get_user_profile_photo_file_name, null=True, blank=True)
    gender = models.IntegerField(verbose_name=_("cinsi"), null=True)
    date_of_birth = models.DateField(default=timezone.now)
    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    # field for checking profile completion on auth register
    is_completed = models.BooleanField(_('completed'), default=False)
    # legacy fields
    old_psw_hash = models.CharField(blank=True, null=True, max_length=300)
    # slug for detail page
    slug = models.SlugField(max_length=255, null=True, blank=True)
    """
        Important non-field stuff
    """
    objects = MyUserManager()

    REQUIRED_FIELDS = []
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = 'İstifadəçi'
        verbose_name_plural = 'İstifadəçilər'

    def __str__(self):
        return "{full_name}".format(
            full_name=self.get_full_name(),
        )

    def save(self, *args, **kwargs):
        super(MyUser, self).save(*args, **kwargs)
        self.slug = slugify(str(self.date_joined.timestamp()))
        super(MyUser, self).save(*args, **kwargs)

    def get_full_name(self):
        """
            Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """
            Returns the short name for the user.
        """
        return self.first_name

    def get_avatar(self):
        if self.profile_picture:
            return mark_safe(
                "<img style='width:100px' src='{}' />".format(self.profile_picture.url)
            )

    def get_profile_picture(self):
        if self.profile_picture:
            return self.profile_picture.url

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def get_absolute_url(self):
        return reverse('account:account-detail', kwargs={'slug': self.slug})

    def get_wishs(self):
        return self.wishes.filter(is_deleted=False)

    def get_wishs_count(self):
        return self.get_wishs().count()

    def get_accumulated_amount(self):
        user_wishs = self.wishes.all()
        final_amount = 0
        for wish in user_wishs:
            final_amount += wish.accumulated_amount
        return final_amount

    def get_number_of_donations(self):
        user_wishs = self.wishes.all()
        final_number = 0
        for wish in user_wishs:
            final_number += wish.number_of_donations
        return final_number
