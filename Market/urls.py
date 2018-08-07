from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from MarketApp import views

urlpatterns = [
    url('^accounts/', include('registration.backends.simple.urls')),
    url('^home$|^$', views.IndexView.as_view(template_name='index.html')),
    url('^brand/(?P<brand_id>\w+)/$', views.BrandPageView.as_view(template_name='brands.html')),
    url('^brand/(?P<brand_id>\w+)/(?P<car_id>\w+)/$', views.CarPageView.as_view(template_name='cars.html')),
    url('^filter/$', views.CarView.car_filter),
    url('^admin/', admin.site.urls),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
                      url(r'^__debug__/', include(debug_toolbar.urls)),
                  ] + urlpatterns
