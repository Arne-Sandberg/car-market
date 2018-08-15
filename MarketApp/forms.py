from django import forms
from django.db.models import Max, Min
from django_range_slider.fields import RangeSliderField
from registration.forms import RegistrationForm
from django.contrib.auth import get_user_model
from MarketApp import models


class FilterForm(forms.Form):
    min_year = forms.IntegerField()
    max_year = forms.IntegerField()
    colour = forms.ChoiceField(required=False)
    number_of_seats = forms.IntegerField(min_value=1, initial=4)
    price = RangeSliderField()
    in_stock_only = forms.BooleanField(required=False)

    def __init__(self, brand_id, *args, **kwargs):
        super(FilterForm, self).__init__(*args, **kwargs)
        cars = models.Car.objects.filter(brand_id=brand_id)
        max_p = cars.aggregate(Max('price'))['price__max']
        min_p = cars.aggregate(Min('price'))['price__min']
        max_y = cars.aggregate(Max('year'))['year__max']
        min_y = cars.aggregate(Min('year'))['year__min']
        choices = [('any colour', 'any colour')]
        car_colours = list(set([(x.colour, x.colour) for x in cars]))
        choices += car_colours
        self.fields['colour'] = forms.ChoiceField(choices=choices, initial='any colour')
        self.fields['price'] = RangeSliderField(label='Price', minimum=min_p, maximum=max_p, name='$')
        self.fields['min_year'] = forms.IntegerField(min_value=min_y, max_value=max_y, initial=min_y)
        self.fields['max_year'] = forms.IntegerField(min_value=min_y, max_value=max_y, initial=max_y)


class UserEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)
        self.fields['image'].required = False

    class Meta:
        model = get_user_model()
        fields = ('image', 'first_name', 'last_name', 'email')


class UserCreateForm(RegistrationForm):
    class Meta:
        model = models.User
        fields = ('username', 'email', 'password1', 'password2')


class CommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ('content', 'rating')
        widgets = {
            'content': forms.Textarea(attrs={'rows': 2}),
        }
