from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from core.options.tools import slugify, AMOUNTS
from django.conf import settings
from django.utils.safestring import mark_safe
from django.contrib.postgres.fields import JSONField, ArrayField
from core.options.tools import EVENT_TYPES
from ckeditor.fields import RichTextField


# Create your models here.

class SiteSettings(models.Model):
    # main page content
    main_page_first_section_title = models.CharField(max_length=255, blank=True, null=True)
    main_page_first_section_text = models.TextField(blank=True, null=True)
    main_page_second_section_title = models.CharField(max_length=255, blank=True, null=True)
    main_page_second_section_text = models.TextField(blank=True, null=True)
    main_page_third_section_title = models.CharField(max_length=255, blank=True, null=True)
    main_page_third_section_text = models.TextField(blank=True, null=True)
    main_page_fourth_section_title = models.CharField(max_length=255, blank=True, null=True)
    main_page_fourth_section_text = models.TextField(blank=True, null=True)
    footer_sign_up_title = models.CharField(max_length=255, blank=True, null=True)
    footer_copyright_text = models.CharField(max_length=255, blank=True, null=True)
    footer_contact_email = models.CharField(max_length=255, blank=True, null=True)
    footer_contact_number = models.CharField(max_length=255, blank=True, null=True)
    # social links
    twitter_profile_url = models.URLField(verbose_name='twitter_hyperlink', blank=True)
    instagram_profile_url = models.URLField(verbose_name='instagram_hyperlink', blank=True)
    facebook_profile_url = models.URLField(verbose_name='facebook_hyperlink', blank=True)
    youtube_profile_url = models.URLField(verbose_name='youtube_hyperlink', blank=True)

    def __str__(self):
        return 'Site Settings'

    class Meta:
        verbose_name = "Site setting"
        verbose_name_plural = "Site settings"


class Wish(models.Model):
    name = models.CharField(_('name'), max_length=255)
    surname = models.CharField(_('surname'), max_length=255)
    title = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('short description'))
    image = models.ImageField(_('image'), upload_to='wish', blank=True, null=True)
    required_amount = models.IntegerField(_('required amount'), default=0)
    currency = models.CharField(_('currency'), max_length=255)
    accumulated_amount = models.IntegerField(_('accumulated amount'), default=0)
    number_of_donations = models.IntegerField(_('number of donations'), default=0)
    deadline = models.DateField(_('deadline'), default=timezone.now)
    video = models.CharField(_('video url'), max_length=255, blank=True, null=True)
    identification_card_image = models.ImageField(upload_to='identification_card_image', null=True, blank=True)
    published = models.BooleanField(_('published'), default=False)
    is_deleted = models.BooleanField(_('deleted'), default=False)
    slug = models.CharField(max_length=255, unique=True, blank=True, null=True)
    event_type = models.ForeignKey('EventType', on_delete=models.CASCADE, related_name='wishes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wishes')
    # moderation
    status = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    # logs
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}".format(self.title)

    def save(self, *args, **kwargs):
        super(Wish, self).save(*args, **kwargs)
        if not self.slug:
            self.slug = slugify(self.title + str(self.created_at.timestamp()))
        else:
            self.slug = slugify(self.slug)
        super(Wish, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('core:detail-wish', kwargs={'slug': self.slug})

    def event_type_title(self):
        return self.event_type.get_title_display()

    def get_cover(self):
        img = self.images.all().first()
        if img:
            return img.url.url

    def get_full_name(self):
        """
            Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.name, self.surname)
        return full_name.strip()

    class Meta:
        ordering = ('-created_at', 'order')
        verbose_name = _('Arzu')
        verbose_name_plural = _('Arzular')


class EventType(models.Model):
    title = models.IntegerField(_('event title'), choices=EVENT_TYPES, default=0)
    extra = JSONField(blank=True, null=True)

    # moderation
    status = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    # logs
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}".format(self.title)

    class Meta:
        verbose_name = _('Tədbirin növü')
        verbose_name_plural = _('Tədbirin növləri')


class Image(models.Model):
    url = models.ImageField(_('Image url'), upload_to='wish_gallery')
    order = models.IntegerField(default=0)
    wish = models.ForeignKey('Wish', on_delete=models.CASCADE, related_name='images', null=True, blank=True)
    # logs
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}'.format(self.url.name)

    def preview_image(self):
        return mark_safe(
            "<img style='width:150px' src='{}' /></p>".format(
                self.url.url, )
        )

    class Meta:
        ordering = ('order',)
        verbose_name = _('Şəkil')
        verbose_name_plural = _('Şəkillər')


class AmountRange(models.Model):
    # amounts = ArrayField(models.IntegerField(default=0))
    event_type = models.ForeignKey('EventType', on_delete=models.CASCADE, related_name='amount_range')
    # logs
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.event_type.title

    class Meta:
        verbose_name = _('Məbləğ aralığı')
        verbose_name_plural = _('Məbləğ aralıqları')


class Donation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='donations')
    wish = models.ForeignKey('Wish', on_delete=models.CASCADE, related_name='donations')
    comment = models.TextField(_('comment for donation'))
    amount = models.IntegerField()
    show_amount = models.BooleanField(default=True)
    currency = models.CharField(max_length=10)
    # logs
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'Donation by {}'.format(self.user.username)

    @property
    def since(self):
        days = (timezone.now() - self.created_at).days
        if days == 0:
            return str(_('today'))
        else:
            return str(days) + str(_(' day ago'))

    @property
    def like_count(self):
        return self.likes.count()

    class Meta:
        verbose_name = _('Bağış (Hədiyyə)')
        verbose_name_plural = _('Bağış (Hədiyyələr)')

    def get_all_replies(self):
        return self.replies.filter(status=True)


class Reply(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='replies')
    comment = models.TextField(_('comment to donation'))
    donation = models.ForeignKey('Donation', on_delete=models.CASCADE, related_name='replies')
    status = models.BooleanField(default=True)
    # logs
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'Reply by {} to donation by {}'.format(self.user.get_full_name(), self.donation.user.get_full_name())

    @property
    def since(self):
        days = (timezone.now() - self.created_at).days
        if days == 0:
            return str(_('today'))
        else:
            return str(days) + str(_(' day ago'))

    @property
    def like_count(self):
        return self.likes.count()

    class Meta:
        verbose_name = _('Bağış commenti')
        verbose_name_plural = _('Bağış commentləri')


class Like(models.Model):
    donation = models.ForeignKey('Donation', on_delete=models.CASCADE, related_name='likes', blank=True, null=True)
    reply = models.ForeignKey('Reply', on_delete=models.CASCADE, related_name='likes', blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='likes')
    # logs
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'Like by {}'.format(self.user.username)

    class Meta:
        verbose_name = _('Bəyənmə')
        verbose_name_plural = _('Bəyənmələr')


class PrivacyPolicy(models.Model):
    content = models.TextField()
    # logs
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'Privacy Policy'

    class Meta:
        verbose_name = _('Privacy Policy')
        verbose_name_plural = _('Privacy Policies')


class Subscribers(models.Model):
    email = models.EmailField(max_length=200, unique=True)
    # logs
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Subscriber'
        verbose_name_plural = 'Subscribers'


class HowItWorks(models.Model):
    content = RichTextField()
    # logs
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "How it works content"

    class Meta:
        verbose_name = 'How It Works'
        verbose_name_plural = 'How It Works'


class Menu(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    url = models.CharField(max_length=255, null=True, blank=True)
    sub_menu = models.ForeignKey('self', related_name='submenus', on_delete=models.CASCADE, null=True, blank=True)
    base = models.BooleanField(default=True)
    order = models.IntegerField()
    status = models.BooleanField(default=True)

    def get_submenus(self):
        sub_menus = Menu.objects.filter(sub_menu=self)
        if sub_menus.last():
            return sub_menus
        else:
            return False

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('order',)
        verbose_name = "Main page menus"
        verbose_name_plural = "Main page menus"
