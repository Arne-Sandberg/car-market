from django.views.generic import TemplateView
from MarketApp import models
from random import sample
from django.views.generic.list import ListView
from django.shortcuts import render


# Create your views here.

class IndexView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['brands'] = models.Brand.objects.all()
        context['advertisement'] = models.Car.objects.filter(is_advertised=True).select_related('brand')
        if len(context['advertisement']) == 0:
            count = models.Car.objects.all().count()
            size = count if count < 6 else 6
            rand_ids = sample(range(1, count + 1), size)
            print(rand_ids, count)
            context['advertisement'] = models.Car.objects.filter(id__in=rand_ids).select_related('brand')
        return context


class BrandView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cars'] = models.Car.objects.filter(brand_id=self.kwargs['brand_id']).select_related(
            'brand').prefetch_related('image_set')
        return context


class CarView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['brands'] = models.Brand.objects.all()
        context['car'] = models.Car.objects.prefetch_related('image_set').get(id=self.kwargs['car_id'])
        return context
