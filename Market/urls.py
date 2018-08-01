from django.contrib import admin
from MarketApp import views
from django.conf.urls import include, url


urlpatterns = [
    url('^login', views.login),
    url('home', views.index),
    url('^signin', views.signin),
    url('$', views.index),
]