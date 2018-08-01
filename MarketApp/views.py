from .forms import SigninForm, LoginForms
from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, 'index.html')


def login(request):
    loginf = LoginForms()
    return render(request, 'forms/form.html', {'form': loginf})


def signin(request):
    signinf = SigninForm()
    return render(request, 'forms/form.html', {'form': signinf})
