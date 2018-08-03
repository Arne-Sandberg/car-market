from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView
from MarketApp import views

urlpatterns = [
    url('^accounts/', include('registration.backends.simple.urls')),
    url('(^home$|^$)', views.IndexView.as_view(template_name='index.html')),
    url('^admin/', admin.site.urls)
]
