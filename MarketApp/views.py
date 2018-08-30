import os
import requests

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.sites.shortcuts import get_current_site
from django.core.files.storage import FileSystemStorage
from django.forms import inlineformset_factory, formset_factory
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import TemplateView, FormView, DetailView, View
from formtools.wizard.views import SessionWizardView
from registration.backends.simple.views import RegistrationView

from Market import settings
from MarketApp import models, forms, tasks
from random import shuffle

from MarketApp.utils import create_charge


class CustomUserRegistration(RegistrationView):
    def register(self, form):
        new_user = super(CustomUserRegistration, self).register(form)
        reciever = new_user.email
        msg = f'Thank you {new_user}, for registration\nYou can view your profile at:\n' + \
              f'http://{ get_current_site(self.request).domain}/accounts/profile/{new_user}'
        tasks.send_message(reciever, 'Registration', msg)
        return new_user


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['brands'] = models.Brand.objects.all()
        context['advertisement'] = models.Car.objects.advertisement()
        if not context['advertisement']:
            ids_list = list(models.Car.objects.all().values_list('id', flat=True))
            shuffle(ids_list)
            context['advertisement'] = models.Car.objects.filter(id__in=ids_list[:6])
        context['advertisement'] = context['advertisement'].select_related('brand').prefetch_related('image_set')
        return context


class BrandView(FormView):
    template_name = 'filter.html'
    form_class = forms.FilterForm

    def get_context_data(self, **kwargs):
        context = super(BrandView, self).get_context_data(**kwargs)
        context['flag'] = 'brand'
        context['brand_name'] = models.Brand.objects.get(id=self.kwargs['brand_id']).name
        context['cars'] = models.Car.objects.filter(brand_id=self.kwargs['brand_id']).select_related(
            'brand').prefetch_related('image_set')
        return context


class SearchView(FormView):
    template_name = 'filter.html'
    form_class = forms.FilterForm

    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        context['flag'] = 'search'
        context['brand_name'] = 'All'
        data = self.request.GET
        context['cars'] = models.Car.objects.search_cars(data.get('search_content'))
        context['search_content'] = data['search_content']
        context['cars'] = context['cars'].select_related('brand').prefetch_related('image_set')
        return context


class BrandContent(TemplateView):
    template_name = 'brand_content.html'

    def get_context_data(self, **kwargs):
        context = super(BrandContent, self).get_context_data(**kwargs)
        data = self.request.GET
        objects = models.Car.objects
        brand_id = int(kwargs['brand_id'])
        form = forms.FilterForm(brand_id, data.get('min_price'), data.get('max_price'), data)
        if kwargs['filter_flag'] == 'submit':
            if form.is_valid():
                context['cars'] = objects.filter_cars(data, brand_id, data['search_content']) if data.get(
                    'search_content') else objects.filter_cars(data, brand_id)
                context['cars'] = context['cars'].select_related('brand').prefetch_related('image_set')
        else:
            context['cars'] = objects.filter(brand_id=kwargs['brand_id']) if brand_id else objects.search_cars(
                data['search_content'])
            context['cars'] = context['cars'].select_related('brand').prefetch_related('image_set')
        if not brand_id:
            context['flag'] = 'search'
            context['search_content'] = data['search_content']
        context['form'] = form
        context['brand_name'] = models.Brand.objects.get(id=brand_id).name if brand_id else 'All'
        return context


class CarView(DetailView):
    template_name = 'car.html'
    model = models.Car

    def get_context_data(self, **kwargs):
        context = super(CarView, self).get_context_data(**kwargs)
        context['brands'] = models.Brand.objects.all()
        context['images'] = self.get_object().image_set.all()
        context['stripe_key'] = settings.STRIPE_PUBLIC_KEY
        context['form'] = forms.CommentForm
        context['comments'] = self.get_object().comment_set.all().select_related('user')
        user = self.get_object().user
        context['flag'] = 'no_button' if user and (
                user == self.request.user or not user.stripe_user_id) else 'show_button'
        return context


class CheckoutResultView(TemplateView):
    template_name = 'checkout_result.html'

    def get_context_data(self, **kwargs):
        context = super(CheckoutResultView, self).get_context_data(**kwargs)
        context['brands'] = models.Brand.objects.all()
        context['car'] = models.Car.objects.get(id=self.kwargs['pk'])
        context['flag'] = self.kwargs['flag']
        return context


class CheckoutView(View):
    def post(self, request, *args, **kwargs):
        result = create_charge(request, kwargs['pk'], request.POST.get("stripeToken"))
        if result:
            car = models.Car.objects.get(id=kwargs['pk'])
            kwargs['flag'] = 'success'
            msg = f'Thank you, for purchasing {car}.\nThe information about purchase would be available at:\n' + \
                  f'http://{get_current_site(request).domain}/accounts/profile/{request.user}'
            tasks.send_message(request.POST.get('stripeEmail'), 'Car purchasing', msg)
        else:
            kwargs['flag'] = 'error'
        return HttpResponseRedirect(reverse('checkout_result', kwargs=kwargs))


class ProfileView(TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context['user'] = models.User.objects.get(username=kwargs['username'])
        return context


class EditProfileView(FormView):
    template_name = 'profile_form.html'
    form_class = forms.UserEditForm

    def get_context_data(self, **kwargs):
        context = super(EditProfileView, self).get_context_data(**kwargs)
        context['flag'] = 'profile' if self.request.user.is_authenticated else 'not_authenticated'
        return context

    def get_form_kwargs(self):
        kwargs = super(EditProfileView, self).get_form_kwargs()
        kwargs['instance'] = self.request.user
        return kwargs

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
        context['flag'] = 'password' if self.request.user.is_authenticated else 'not_authenticated'
        return context

    def form_valid(self, form):
        user = form.save()
        update_session_auth_hash(self.request, user)
        return HttpResponseRedirect(reverse('profile', kwargs={'username': self.request.user}))


class StripeConnectView(TemplateView):
    template_name = 'profile_form.html'

    def get_context_data(self, **kwargs):
        context = super(StripeConnectView, self).get_context_data(**kwargs)
        code = self.request.GET.get('code')
        data = {'client_secret': settings.STRIPE_SECRET_KEY, 'code': code, 'grant_type': 'authorization_code'}
        response = requests.post('https://connect.stripe.com/oauth/token', params=data).json()
        if response.get('stripe_user_id'):
            self.request.user.stripe_user_id = response['stripe_user_id']
            self.request.user.save()
            context['flag'] = 'stripe_success'
        else:
            context['flag'] = 'stripe_error'
        return context


class CommentContent(TemplateView):
    template_name = 'comments.html'

    def post(self, request, *args, **kwargs):
        data = request.POST
        form = forms.CommentForm(data)
        context = self.get_context_data()
        context['comments'] = models.Car.objects.get(id=data['car_id']).comment_set.all().select_related('user')
        context['form'] = forms.CommentForm()
        if data.get('flag') == 'delete':
            models.Comment.objects.get(id=data.get('comment_id')).delete()
        elif data.get('flag') == 'edit':
            if form.is_valid():
                forms.CommentForm(data, instance=models.Comment.objects.get(id=data.get('comment_id'))).save()
            else:
                context['editing_comment_id'] = data.get('comment_id')
                context['form'] = form
        elif data.get('flag') == 'create':
            if form.is_valid():
                comment = form.save(commit=False)
                comment.car_id = data.get('car_id')
                comment.user = self.request.user
                comment.save()
            else:
                context['form'] = form
        elif data.get('flag') == 'editing':
            context['editing_comment_id'] = data.get('comment_id')
            context['form'] = forms.CommentForm(data, instance=models.Comment.objects.get(id=data.get('comment_id')))
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
        car.user = self.request.user
        car.save()
        for image_form in form_data[1]:
            if image_form.cleaned_data:
                image = image_form.save(commit=False)
                image.car = car
                image.save()
                self.file_storage.delete(image_form.cleaned_data['image'])
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
        elif car.user != self.request.user:
            context['flag'] = 'editing_not_allowed'
        return context

    def get_form_instance(self, step):
        return models.Car.objects.get(id=self.kwargs['car_id'])

    def done(self, form_list, **kwargs):
        form_data = [form for form in form_list]
        form_data[0].save()
        for image_form in form_data[1]:
            if image_form.cleaned_data:
                image_form.save()
                self.file_storage.delete(image_form.cleaned_data['image'])
        return HttpResponseRedirect(reverse('profile', kwargs={'username': self.request.user}))


class DeleteCarView(TemplateView):
    template_name = 'users_cars.html'

    def post(self, request, *args, **kwargs):
        models.Car.objects.get(id=request.POST['car_id']).delete()
        context = self.get_context_data()
        context['user'] = self.request.user
        return self.render_to_response(context)
