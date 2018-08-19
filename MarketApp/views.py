import os

import requests

import stripe
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.core.files.storage import FileSystemStorage
from django.forms import modelformset_factory, inlineformset_factory, formset_factory
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.views.generic import TemplateView, FormView, DetailView
from django.views.generic.base import View
from formtools.wizard.views import WizardView, SessionWizardView

from Market import settings
from MarketApp import models, forms
from random import shuffle


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['brands'] = models.Brand.objects.all()
        context['advertisement'] = models.Car.objects.filter(is_advertised=True)
        if not context['advertisement']:
            ids_list = list(models.Car.objects.all().values_list('id', flat=True))
            shuffle(ids_list)
            context['advertisement'] = models.Car.objects.filter(id__in=ids_list[:6]).select_related(
                'brand').prefetch_related('image_set')
        return context


class BrandView(FormView):
    template_name = 'brands.html'
    form_class = forms.FilterForm

    def get_context_data(self, **kwargs):
        context = super(BrandView, self).get_context_data(**kwargs)
        context['brand_name'] = models.Brand.objects.get(id=self.kwargs['brand_id']).name
        context['cars'] = models.Car.objects.filter(brand_id=self.kwargs['brand_id']).select_related(
            'brand').prefetch_related('image_set')
        return context

    def get_form_kwargs(self):
        kwargs = super(BrandView, self).get_form_kwargs()
        kwargs['brand_id'] = self.kwargs['brand_id']
        return kwargs


class BrandContent(TemplateView):
    template_name = 'brand_content.html'

    def get_context_data(self, **kwargs):
        context = super(BrandContent, self).get_context_data(**kwargs)
        context['brand_name'] = models.Brand.objects.get(id=self.kwargs['brand_id']).name
        data = self.request.GET
        if data:
            context['cars'] = models.Car.objects.filter(brand_id=self.kwargs['brand_id'])
            if data['colour'] != 'any colour':
                context['cars'] = context['cars'].filter(colour=data['colour'])
            if data['in_stock_only']:
                context['cars'] = context['cars'].filter(stock_count__gt=0)
            context['cars'] = context['cars'].filter(year__lte=data['max_year'], year__gte=data['min_year'],
                                                     number_of_seats=data['number_of_seats'],
                                                     price__gte=data['min_price'],
                                                     price__lte=data['max_price']).select_related(
                'brand').prefetch_related('image_set')
        else:
            context['cars'] = models.Car.objects.filter(brand_id=self.kwargs['brand_id']).select_related(
                'brand').prefetch_related('image_set')
        return context


class CarView(DetailView):
    template_name = 'cars.html'
    model = models.Car

    def get_context_data(self, **kwargs):
        context = super(CarView, self).get_context_data(**kwargs)
        context['brands'] = models.Brand.objects.all()
        context['images'] = context['object'].image_set.all()
        context['stripe_key'] = settings.STRIPE_PUBLIC_KEY
        context['flag'] = 'show_button'
        context['form'] = forms.CommentForm
        owner = context['object'].owner
        if owner and (owner == self.request.user or not owner.stripe_user_id):
            context['flag'] = 'no_button'
        return context


class ThanksView(TemplateView):
    template_name = 'thanks.html'

    def get_context_data(self, **kwargs):
        context = super(ThanksView, self).get_context_data(**kwargs)
        context['brands'] = models.Brand.objects.all()
        context['car'] = models.Car.objects.get(id=self.kwargs['pk'])
        return context


class ErrorView(TemplateView):
    template_name = 'error.html'

    def get_context_data(self, **kwargs):
        context = super(ErrorView, self).get_context_data(**kwargs)
        context['brands'] = models.Brand.objects.all()
        return context


class CheckoutView(View):
    def post(self, request, *args, **kwargs):
        token = request.POST.get("stripeToken")
        car = models.Car.objects.get(id=kwargs['pk'])
        car.stock_count -= 1
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            if car.owner:
                stripe.Charge.create(
                    amount=int(car.price * 92.9 + 30),
                    currency="usd",
                    source=token,
                    description=f"{car} {car.colour} was sold to {request.user}",
                    application_fee=int(car.price * 7.1 - 30),
                    stripe_account=car.owner.stripe_user_id,
                )
            else:
                stripe.Charge.create(
                    amount=car.price * 100,
                    currency="usd",
                    source=token,
                    description=f"{car} {car.colour} was sold to {request.user}",
                )
        except stripe.error.CardError:
            return HttpResponseRedirect(reverse('error', kwargs=kwargs))
        else:
            models.Purchase.objects.create(user=request.user, price=car.price, date=timezone.now(), car=car)
            car.save()
            return HttpResponseRedirect(reverse('thanks', kwargs=kwargs))


class ProfileView(TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context['user'] = models.User.objects.get(username=self.kwargs['username'])
        return context


class EditProfileView(FormView):
    template_name = 'profile_form.html'
    form_class = forms.UserEditForm

    def get_context_data(self, **kwargs):
        context = super(EditProfileView, self).get_context_data(**kwargs)
        if not self.request.user.is_authenticated:
            context['flag'] = 'not_authenticated'
        else:
            context['form'] = forms.UserEditForm(instance=self.request.user)
        return context

    def form_valid(self, form):
        forms.UserEditForm(self.request.POST, self.request.FILES, instance=self.request.user).save()
        return HttpResponseRedirect(reverse('profile', kwargs={'username': self.request.user}))


class EditPasswordView(FormView):
    template_name = 'profile_form.html'
    form_class = PasswordChangeForm

    def get_form_kwargs(self):
        kwargs = super(EditPasswordView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(EditPasswordView, self).get_context_data(**kwargs)
        if not self.request.user.is_authenticated:
            context['flag'] = 'not_authenticated'
        return context

    def form_valid(self, form):
        user = form.save()
        update_session_auth_hash(self.request, user)
        return HttpResponseRedirect(reverse('profile', kwargs={'username': self.request.user}))


class CommentContent(TemplateView):
    template_name = 'comment.html'

    def post(self, request, *args, **kwargs):
        data = request.POST
        form = forms.CommentForm(data)
        context = self.get_context_data()
        context['object'] = models.Car.objects.get(id=data['car_id'])
        context['form'] = forms.CommentForm()
        if data['flag'] == 'delete':
            models.Comment.objects.get(id=data['comment_id']).delete()
        elif data['flag'] == 'edit':
            if form.is_valid():
                forms.CommentForm(data, instance=models.Comment.objects.get(id=data['comment_id'])).save()
            else:
                context['editing_comment_id'] = int(data['comment_id'])
                context['form'] = form
        elif data['flag'] == 'create':
            if form.is_valid():
                comment = form.save(commit=False)
                comment.car_id = data['car_id']
                comment.user = self.request.user
                comment.save()
            else:
                context['form'] = form
        elif data['flag'] == 'editing':
            context['editing_comment_id'] = int(data['comment_id'])
            initial = {'content': data['content'], 'rating': data['rating']}
            context['form'] = forms.CommentForm(initial=initial)
        return self.render_to_response(context)


class CreateCarView(SessionWizardView):
    template_name = 'car_form.html'
    form_list = [forms.CarForm, formset_factory(form=forms.ImageForm, extra=3)]
    file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'storage'))

    def get_context_data(self, **kwargs):
        context = super(CreateCarView, self).get_context_data(**kwargs)
        if not self.request.user.is_authenticated:
            context['flag'] = 'not_authenticated'
        elif not self.request.user.stripe_user_id:
            context['flag'] = 'no_keys'
        return context

    def done(self, form_list, **kwargs):
        form_data = [form for form in form_list]
        car = form_data[0].save(commit=False)
        car.owner = self.request.user
        car.save()
        for data in form_data[1]:
            if data.cleaned_data:
                image = data.save(commit=False)
                image.car = car
                image.save()
        return HttpResponseRedirect(reverse('profile', kwargs={'username': self.request.user}))


class EditCarView(SessionWizardView):
    template_name = 'car_form.html'
    form_list = [forms.CarForm, inlineformset_factory(models.Car, models.Image, forms.ImageForm, extra=1)]
    file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'storage'))

    def get_context_data(self, **kwargs):
        context = super(EditCarView, self).get_context_data(**kwargs)
        car = models.Car.objects.get(id=self.kwargs['car_id'])
        context['user'] = self.request.user
        if not self.request.user.stripe_user_id:
            context['flag'] = 'no_keys'
        elif car.owner != self.request.user:
            context['flag'] = 'editing_not_allowed'
        return context

    def get_form_instance(self, step):
        return models.Car.objects.get(id=self.kwargs['car_id'])

    def done(self, form_list, **kwargs):
        form_data = [form for form in form_list]
        form_data[0].save()
        for data in form_data[1]:
            if data.cleaned_data:
                data.save()
        return HttpResponseRedirect(reverse('profile', kwargs={'username': self.request.user}))


class UserProfileView(TemplateView):
    template_name = 'profile_form.html'

    def get_context_data(self, **kwargs):
        context = super(UserProfileView, self).get_context_data(**kwargs)
        code = self.request.GET['code']
        data = {'client_secret': settings.STRIPE_SECRET_KEY, 'code': code, 'grant_type': 'authorization_code'}
        response = requests.post('https://connect.stripe.com/oauth/token', params=data).json()
        if 'stripe_user_id' in response:
            self.request.user.stripe_user_id = response['stripe_user_id']
            self.request.user.save()
            context['flag'] = 'stripe_success'
        else:
            context['flag'] = 'stripe_error'
        return context


class DeleteCarView(TemplateView):
    template_name = 'users_cars.html'

    def post(self, request, *args, **kwargs):
        models.Car.objects.get(id=request.POST['car_id']).delete()
        context = self.get_context_data()
        context['user'] = self.request.user
        return self.render_to_response(context)
