from django.views.generic import TemplateView
from MarketApp import models
from django.shortcuts import render


# Create your views here.

class IndexView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['brands'] = models.Brand.objects.all()
        return context


class BrandView(TemplateView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cars'] = models.Car.objects.filter(brand__name=self.kwargs['brand_name'])
        context['cars_names'] = []
        for c in context['cars']:
            print(c.image_set)

        return context
