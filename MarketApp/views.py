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
            # print(rand_ids, count)
            context['advertisement'] = models.Car.objects.filter(id__in=rand_ids).select_related(
                'brand').prefetch_related('image_set')
        return context


class BrandPageView(FormView):
    template_name = 'brand_content.html'
    success_url = '/home'
    form_class = forms.FilterForm

    def get_context_data(self, **kwargs):
        context = super(BrandPageView, self).get_context_data(**kwargs)
        context['brand_name'] = models.Brand.objects.get(id=self.kwargs['brand_id']).name
        context['cars'] = models.Car.objects.filter(brand_id=self.kwargs['brand_id']).select_related(
            'brand').prefetch_related('image_set')
        return context

    def get_form_kwargs(self):
        kwargs = super(BrandPageView, self).get_form_kwargs()
        kwargs['brand_id'] = self.kwargs['brand_id']
        return kwargs

    def car_filter(self, request):
        data = dict(**request.GET)
        cars = models.Car.objects.filter(brand__name=data['brand_name'][0])

        if data['colour'][0] != 'any colour':
            cars = cars.filter(colour=data['colour'][0])
        if data['in_stock_only'][0]:
            cars = cars.filter(stock_count__gt=0)
        cars = cars.filter(year__lte=int(data['max_year'][0]), year__gte=int(data['min_year'][0]),
                           number_of_seats=int(data['number_of_seats'][0]),
                           price__gte=int(data['min_price'][0].strip()),
                           price__lte=int(data['max_price'][0].strip())).select_related(
            'brand').prefetch_related('image_set')
        print(len(cars))
        return cars


class CarPageView(TemplateView):
    template_name = 'cars.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['brands'] = models.Brand.objects.all()
        context['car'] = models.Car.objects.prefetch_related('image_set').get(id=self.kwargs['car_id'])
        return context
