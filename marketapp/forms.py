import re

from django import forms
from django.db.models import Max, Min
from django.utils import timezone
from registration.forms import RegistrationFormUniqueEmail
from django.contrib.auth import get_user_model
from marketapp import models
from django.utils.safestring import mark_safe


class RangeSlider(forms.TextInput):
    def __init__(self, minimum, maximum, elem_name, min_val, max_val, *args, **kwargs):
        super(RangeSlider, self).__init__(*args, **kwargs)
        self.min_val = str(min_val) if min_val else str(minimum)
        self.max_val = str(max_val) if max_val else str(maximum)
        self.minimum = str(minimum)
        self.maximum = str(maximum)
        self.elem_name = str(elem_name)

    def render(self, name, value, attrs=None, renderer=None):
        s = super(RangeSlider, self).render(name, value, attrs)
        elem_id = re.findall(r'id_([A-Za-z0-9_\./\\-]*)"', s)[0]
        html = """<div id="slider-range-""" + elem_id + """"></div>
        <script>
        $('#id_""" + elem_id + """').attr("readonly", true)
        $( "#slider-range-""" + elem_id + """" ).slider({
        range: true,
        min: """ + self.minimum + """,
        max: """ + self.maximum + """,
        values: [ """ + self.min_val + """,""" + self.max_val + """ ],
        slide: function( event, ui ) {
          $( "#id_""" + elem_id + """" ).val(" """ + self.elem_name + """ "+ ui.values[ 0 ] + " - " + ui.values[ 1 ] );
        }
        });
        $( "#id_""" + elem_id + """" ).val(" """ + self.elem_name + """ "+ $( "#slider-range-""" + elem_id + """" ).slider( "values", 0 ) +
        " - " + $( "#slider-range-""" + elem_id + """" ).slider( "values", 1 ) );
        </script>
        """
        return mark_safe(s + html)


class RangeSliderField(forms.CharField):
    def __init__(self, *args, **kwargs):
        self.name = kwargs.pop('name', '')
        self.minimum = kwargs.pop('minimum', 0)
        self.maximum = kwargs.pop('maximum', 100)
        self.min_val = kwargs.pop('min_val', 0)
        self.max_val = kwargs.pop('max_val', 0)
        kwargs['widget'] = RangeSlider(self.minimum, self.maximum, self.name, self.min_val, self.max_val)
        if 'label' not in kwargs.keys():
            kwargs['label'] = False
        super(RangeSliderField, self).__init__(*args, **kwargs)


class FilterForm(forms.Form):
    min_year = forms.IntegerField()
    max_year = forms.IntegerField()
    colour = forms.ChoiceField()
    number_of_seats = forms.IntegerField(min_value=1, initial=4)
    price = RangeSliderField()
    in_stock_only = forms.BooleanField(required=False)

    def __init__(self, brand_id=0, min_val=0, max_val=0, *args, **kwargs):
        super(FilterForm, self).__init__(*args, **kwargs)
        cars = models.Car.objects.filter(brand_id=brand_id) if brand_id else models.Car.objects.all()
        max_p = cars.aggregate(Max('price'))['price__max']
        min_p = cars.aggregate(Min('price'))['price__min']
        max_y = cars.aggregate(Max('year'))['year__max']
        min_y = cars.aggregate(Min('year'))['year__min']
        choices = [('any colour', 'any colour')] + list(set([(x.colour, x.colour) for x in cars]))
        self.fields['colour'] = forms.ChoiceField(choices=choices, initial='any colour')
        self.fields['min_year'] = forms.IntegerField(min_value=1, initial=min_y)
        self.fields['max_year'] = forms.IntegerField(min_value=1, initial=max_y)
        self.fields['price'] = RangeSliderField(label='Price', minimum=min_p, maximum=max_p, min_val=min_val,
                                                max_val=max_val, name='$', required=False)


class UserEditForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('image', 'email', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)
        self.fields['image'].required = False


class UserCreateForm(RegistrationFormUniqueEmail):
    class Meta:
        model = models.User
        fields = ('username', 'email', 'password1', 'password2', 'image')


class CommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ('content', 'rating')
        widgets = {'content': forms.Textarea(attrs={'rows': 2}), }

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['rating'] = forms.IntegerField(max_value=5, min_value=1, initial=1)


class ImageForm(forms.ModelForm):
    class Meta:
        model = models.Image
        fields = ('image',)

    def __init__(self, *args, **kwargs):
        super(ImageForm, self).__init__(*args, **kwargs)
        self.fields['image'].required = False


class CarForm(forms.ModelForm):
    class Meta:
        model = models.Car
        fields = ('car_model', 'car_type', 'year', 'number_of_seats', 'colour', 'description', 'stock_count', 'price',
                  'brand',)

    def __init__(self, *args, **kwargs):
        super(CarForm, self).__init__(*args, **kwargs)
        self.fields['description'].required = False
        self.fields['year'] = forms.IntegerField(max_value=timezone.now().year, min_value=0)
        self.fields['number_of_seats'] = forms.IntegerField(max_value=100, min_value=1, initial=4)
        self.fields['stock_count'] = forms.IntegerField(min_value=1, initial=1)
        self.fields['price'] = forms.IntegerField(min_value=100, initial=100)
