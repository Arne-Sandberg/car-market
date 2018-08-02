from django.views.generic import TemplateView
from MarketApp import models
from django.shortcuts import render


# Create your views here.

class IndexView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data'] = models.Brand.objects.all()
        return context
