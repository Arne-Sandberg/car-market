from django.conf.urls import include, url
from django.views.generic import TemplateView

urlpatterns = [
    url('^accounts/', include('registration.backends.simple.urls')),
    url('(^home$|^$)', TemplateView.as_view(template_name='index.html')),
]
