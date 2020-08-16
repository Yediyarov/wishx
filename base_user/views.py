import logging
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from django.forms import forms
from django.contrib import messages
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth import views
from django.views.generic import UpdateView, DetailView
# from django.views.generic.edit import UpdateView
from base_user.forms import BaseRegistrationForm, MyUserLoginForm, AccountEditForm, AccountUpdateForm
from base_user.tools.login_helper_view import AuthView, AccountCompleteRequired
from base_user.tools.token import account_activation_token
import bcrypt
from django.contrib.auth import (login as auth_login)
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
import datetime
from django.contrib.auth.mixins import LoginRequiredMixin


User = get_user_model()
logr = logging.getLogger(__name__)


class AccountBaseLoginView(views.LoginView):
    """
        Account Login View if user is login
        Return to dashboard view
    """
    template_name = "account/login.html"
    form_class = MyUserLoginForm

    def get(self, request, *args, **kwargs):
        """
        Redirect to dashboard if user is authenticated
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        if request.user.is_authenticated:
            return redirect(reverse_lazy('account:account-detail', kwargs={'slug': request.user.slug}))
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('account:account-detail', kwargs={'slug': self.request.user.slug})

    def form_invalid(self, form, *args, **kwargs):
        """
            Check old password before returning error
        """
        return self.check_old_password_before_err(form)

    def check_old_password_before_err(self, form):
        """Check old db password"""
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = User.objects.filter(email=username).first()
        logr.debug("invalid user: %s" % user)

        if password and user is not None and user.old_psw_hash:

            # check if old password matches
            if bcrypt.checkpw(password.encode('utf-8'), user.old_psw_hash.encode('utf-8')):
                # set password as new password
                user.set_password(password)
                user.save()
                # set remember me
                if not self.request.POST.get('remember_me'):
                    self.request.session.set_expiry(1209600)  # remember me session expire in 2 weeks
                # login user
                auth_login(self.request, user)
                return HttpResponseRedirect(self.get_success_url())

        return super().form_invalid(form)


class AccountRegistrationView(AuthView, generic.CreateView):
    """
        Account Register View if user is login
        Return to dashboard view
    """
    template_name = "account/register.html"
    form_class = BaseRegistrationForm
    model = User
    success_url = reverse_lazy("account:register-done")
    user = None

    @staticmethod
    def get_tokens(user):
        return {
            'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
            'token': account_activation_token.make_token(user),
        }

    def send_mail(self, user):
        if user:
            current_site = get_current_site(self.request)
            mail_subject = _('Hesabınızı aktivləşdirin')
            tokens = self.get_tokens(user)
            message = render_to_string('account/email/activation.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': tokens['uid'],
                'token': tokens['token'],
                'protocol': 'https' if self.request.is_secure() else 'http',
            })
            email = EmailMessage(
                mail_subject, message, to=[user.email]
            )
            email.send()

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        birth_day = form.data.get('day', None)
        birth_month = form.data.get('month', None)
        birth_year = form.data.get('year', None)
        if birth_day and birth_month and birth_year:
            try:
                birth_day = int(birth_day)
                birth_month = int(birth_month)
                birth_year = int(birth_year)
                user.date_of_birth = datetime.date(birth_year, birth_month, birth_day)
            except ValueError:
                # pass
                # raise forms.ValidationError("Register details are incorrect")
                # messages.error(self.request, "Register details are incorrect")
                return super().form_invalid(form)

        user.save()
        self.send_mail(user)
        return super().form_valid(form)


class AccountRegistrationDoneView(generic.TemplateView):
    template_name = 'account/register-done.html'


class AccountRegistrationConfirmView(generic.TemplateView):
    template_name = 'account/register-confirm.html'
    user = None
    error = None

    @staticmethod
    def get_user(uidb64):
        try:
            # urlsafe_base64_decode() decodes to bytestring
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        return user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['error'] = self.error
        return context

    def get(self, request, *args, **kwargs):
        self.user = self.get_user(kwargs['uidb64'])
        if self.user:
            if account_activation_token.check_token(self.user, kwargs['token']):
                self.user.is_active = True
                self.user.is_completed = True
                self.user.save()
            else:
                self.error = 'Token failed'
        else:
            self.error = 'user not found'

        return super().get(request, *args, **kwargs)


class ForgetPasswordView(views.PasswordResetView):
    """
        Forget password view
    """
    template_name = "account/forget.html"
    subject_template_name = 'account/email/password_reset_subject.txt'
    email_template_name = 'account/email/password_reset_email.html'
    success_url = reverse_lazy('account:forget-done')


class ForgetPasswordDoneView(views.PasswordResetDoneView):
    """
        Forget password done view
    """
    template_name = "account/forget-done.html"


class ForgetPasswordResetConfirmView(views.PasswordResetConfirmView):
    """
        Forget password view
    """
    template_name = "account/forget-confirm.html"
    post_reset_login = True
    post_reset_login_backend = 'django.contrib.auth.backends.AllowAllUsersModelBackend'
    success_url = reverse_lazy('account:login')


class AccountEditView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'account/edit-account.html'
    form_class = AccountEditForm

    def get(self, request, *args, **kwargs):
        if self.request.user.is_completed:
            return redirect(reverse_lazy('account:account-detail', kwargs={'slug': self.request.user.slug}))
        else:
            return super().get(self)

    def form_valid(self, form):
        user = form.save(commit=False)

        birth_day = form.data.get('day', None)
        birth_month = form.data.get('month', None)
        birth_year = form.data.get('year', None)
        if birth_day and birth_month and birth_year:
            try:
                birth_day = int(birth_day)
                birth_month = int(birth_month)
                birth_year = int(birth_year)
                user.date_of_birth = datetime.date(birth_year, birth_month, birth_day)
            except ValueError:

                return super().form_invalid(form)
        user.is_completed = True
        user.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)

        return super().form_invalid(form)

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, _("Məlumatlar uğurla yeniləndi"))
        return reverse_lazy('account:account-detail', kwargs={'slug': self.object.slug})

    def get_object(self):
        return self.request.user

    def get_form_kwargs(self):
        kwargs = super(AccountEditView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


class AccountDetailView(AccountCompleteRequired, LoginRequiredMixin, DetailView):
    model = User
    template_name = 'account/detail.html'
    context_object_name = 'user'


class AccountUpdateView(AccountCompleteRequired, LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'account/update-account.html'
    form_class = AccountUpdateForm

    def form_valid(self, form):
        user = form.save(commit=False)

        birth_day = form.data.get('day', None)
        birth_month = form.data.get('month', None)
        birth_year = form.data.get('year', None)
        if birth_day and birth_month and birth_year:
            try:
                birth_day = int(birth_day)
                birth_month = int(birth_month)
                birth_year = int(birth_year)
                user.date_of_birth = datetime.date(birth_year, birth_month, birth_day)
            except ValueError:
                return super().form_invalid(form)
        user.save()
        return super().form_valid(form)

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, _("Məlumatlar uğurla yeniləndi"))
        return reverse_lazy('account:account-detail', kwargs={'slug': self.object.slug})

    def get_object(self):
        return self.request.user

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs
