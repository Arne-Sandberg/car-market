from django import forms
from django.db.models import Max, Min
from django_range_slider.fields import RangeSliderField
from MarketApp import models


class FilterForm(forms.Form):
    def __init__(self, brand_id, *args, **kwargs):
        super(FilterForm, self).__init__(*args, **kwargs)
        cars = models.Car.objects.filter(brand_id=brand_id)
        max_d = cars.aggregate(Max('price'))
        min_d = cars.aggregate(Min('price'))
        choices = [('any colour', 'any colour')]
        for car in cars:
            elem = tuple([car.colour, car.colour])
            if elem not in choices:
                choices.append(elem)
        self.fields['colour'] = forms.ChoiceField(choices=choices, initial='any colour')
        self.fields['price'] = RangeSliderField(label='Price', minimum=min_d['price__min'], maximum=max_d[
            'price__max'])

    min_year = forms.IntegerField(min_value=1800, max_value=3000, initial=1800)
    max_year = forms.IntegerField(min_value=1800, max_value=3000, initial=3000)
    colour = forms.ChoiceField(required=False)
    number_of_seats = forms.IntegerField(min_value=1, initial=4)
    price = RangeSliderField()
    in_stock_only = forms.BooleanField(required=False)
