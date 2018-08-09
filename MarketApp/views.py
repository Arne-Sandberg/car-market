from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.generic import TemplateView, FormView
from MarketApp import models
from random import sample
from MarketApp import forms


# Create your views here.

class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['brands'] = models.Brand.objects.all()
        context['advertisement'] = models.Car.objects.filter(is_advertised=True).select_related(
            'brand').prefetch_related('image_set')
        if len(context['advertisement']) == 0:
            count = len(models.Car.objects.all())
            size = count if count < 6 else 6
            rand_ids = sample(range(1, count + 1), size)
            context['advertisement'] = models.Car.objects.filter(id__in=rand_ids).select_related(
                'brand').prefetch_related('image_set')
        return context


class BrandPageView(FormView):
    template_name = 'brands.html'
    form_class = forms.FilterForm

    def form_valid(self, form):
        return self.render_to_response(self.get_context_data())

    def get_context_data(self, **kwargs):
        context = super(BrandPageView, self).get_context_data(**kwargs)
        context['brand_name'] = models.Brand.objects.get(id=self.kwargs['brand_id']).name
        context['cars'] = models.Car.objects.filter(brand_id=self.kwargs['brand_id']).select_related(
            'brand').prefetch_related('image_set')
        # print(len(context['cars']))
        return context

    def get_form_kwargs(self):
        kwargs = super(BrandPageView, self).get_form_kwargs()
        kwargs['brand_id'] = self.kwargs['brand_id']
        return kwargs


class BrandContent(TemplateView):
    template_name = 'brand_content.html'

    def get_context_data(self, **kwargs):
        context = super(BrandContent, self).get_context_data(**kwargs)
        context['brand_name'] = models.Brand.objects.get(id=self.kwargs['brand_id']).name
        data = dict(**self.request.GET)

        context['cars'] = models.Car.objects.filter(brand_id=self.kwargs['brand_id'])
        if data['colour'][0] != 'any colour':
            context['cars'] = context['cars'].filter(colour=data['colour'][0])
        if data['in_stock_only'][0]:
            context['cars'] = context['cars'].filter(stock_count__gt=0)
        context['cars'] = context['cars'].filter(year__lte=data['max_year'][0], year__gte=data['min_year'][0],
                                                 number_of_seats=data['number_of_seats'][0],
                                                 price__gte=data['min_price'][0],
                                                 price__lte=data['max_price'][0]).select_related(
            'brand').prefetch_related('image_set')
        return context


class CarPageView(TemplateView):
    template_name = 'cars.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['brands'] = models.Brand.objects.all()
        context['car'] = models.Car.objects.prefetch_related('image_set').get(id=self.kwargs['car_id'])
        return context
