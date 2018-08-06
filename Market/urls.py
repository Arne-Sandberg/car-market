from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView
from django.conf import settings
from MarketApp import views

urlpatterns = [
    url('^accounts/', include('registration.backends.simple.urls')),
    url('^home$|^$', views.IndexView.as_view(template_name='index.html')),
    url('^brand/(?P<brand_id>\w+)/$', views.BrandView.as_view(template_name='brands.html')),
    url('^brand/(?P<brand_id>\w+)/(?P<car_id>\w+)/$', views.CarView.as_view(template_name='cars.html')),
    url('^admin/', admin.site.urls),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
                      url(r'^__debug__/', include(debug_toolbar.urls)),
                  ] + urlpatterns
