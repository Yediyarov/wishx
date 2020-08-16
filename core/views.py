from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import *
from base_user.tools.login_helper_view import AccountCompleteRequired
from core.forms import *
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.contrib.auth.mixins import UserPassesTestMixin
from datetime import date


# Create your views here.

class BaseIndexView(TemplateView):
    template_name = 'home/index.html'

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(reverse_lazy('account:account-detail', kwargs={'slug': self.request.user.slug}))
        else:
            return super().get(request)


class WishCreateView(AccountCompleteRequired, LoginRequiredMixin, UserPassesTestMixin, CreateView):
    form_class = WishCreationForm
    template_name = 'wish/create.html'
    event_type_model = EventType

    def test_func(self):
        date_of_birth = self.request.user.date_of_birth
        today = date.today()
        day = date_of_birth.day
        month = date_of_birth.month
        if month == 2 and day == 29:
            day = 28

        birthday = date(today.year, month, day)
        days_until_birthday = (birthday - today).days
        if 60 > days_until_birthday > 0:
            return True

    def form_valid(self, form):
        action = self.request.POST.get('publish', None)
        files = self.request.FILES.getlist('multi_image', None)
        wish = form.save(commit=False)
        wish.user = self.request.user
        birthday_event = self.event_type_model.objects.get(title=0)
        wish.event_type = birthday_event
        wish.deadline = self.request.user.date_of_birth
        if action == 'publish':
            wish.published = True
        wish.save()
        if files:
            for f in files:
                Image.objects.create(url=f, wish=wish)
        return super().form_valid(form)

    def get_initial(self):
        self.initial.update(
            {'name': self.request.user.first_name,
             'surname': self.request.user.last_name}
        )
        return super(WishCreateView, self).get_initial()

    def get_success_url(self):
        return reverse_lazy('account:account-detail', kwargs={'slug': self.request.user.slug})

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)


class WishesListView(AccountCompleteRequired, LoginRequiredMixin, ListView):
    model = Wish
    template_name = 'wish/wishes.html'
    context_object_name = 'wishes'
    paginate_by = 8

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = self.get_queryset()
        context['wishes_count'] = self.get_queryset().count()
        page = self.request.GET.get('page', 1) if self.request.GET.get('page', 1) != '' else 1
        paginator = Paginator(data, self.paginate_by)
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(published=True, is_deleted=False)
        return qs


class WishUpdateView(AccountCompleteRequired, LoginRequiredMixin, UpdateView):
    model = Wish
    template_name = 'wish/update.html'
    form_class = WishCreationForm

    def form_valid(self, form):
        action = self.request.POST.get('publish', None)
        if action == 'publish':
            self.object.published = True
        files = self.request.FILES.getlist('multi_image')
        for f in files:
            Image.objects.create(url=f, wish=self.object)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('account:account-detail', kwargs={'slug': self.object.user.slug})


class WishDetailView(DetailView):
    model = Wish
    template_name = 'wish/detail.html'
    context_object_name = 'wish'


class WishAjaxView(View):
    ajax_template = 'partials/wishes.html'

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            page = request.GET.get('page', False)
            if page:
                wish_list = Wish.objects.filter(published=True, is_deleted=False)
                paginator = Paginator(wish_list, 8)
                wishes = paginator.get_page(page)
            else:
                wishes = {}
            return render(request, self.ajax_template, {'wishes': wishes, 'has_next': wishes.has_next()})
        else:
            return JsonResponse({
                "error": "Method not allowed"
            }, status=405)


class WishDeleteView(View):

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            slug = request.GET.get('slug', False)
            print(slug)
            if slug:
                wish = Wish.objects.get(slug=slug)
                wish.is_deleted = True
                wish.save()
                return HttpResponse(status=200)
        else:
            return JsonResponse({
                "error": "Method not allowed"
            }, status=405)


class ComingSoonView(TemplateView):
    template_name = 'additional/coming-soon.html'


class PrivacyPolicyView(ListView):
    model = PrivacyPolicy
    template_name = 'additional/privacy-policy.html'
    context_object_name = 'privacy_policy'


class SubscribeView(CreateView):
    form_class = SubscribeForm
    success_url = reverse_lazy('core:base-index')

    def get(self, request, *args, **kwargs):
        return redirect(self.success_url)

    def form_valid(self, form):
        if self.request.is_ajax():
            subscribe = form.save()
            subscribe.reference_url = self.request.POST.get("reference_url")
            subscribe.save()
            return JsonResponse({
                "save": True
            })

    def form_invalid(self, form):
        return JsonResponse({
            "save": False,
            "message": form.errors
        })


class HowItWorksView(TemplateView):
    template_name = 'additional/howitworks.html'
