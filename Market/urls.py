from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from MarketApp import views

urlpatterns = [
    url('^accounts/', include('registration.backends.simple.urls')),
    url('^home$|^$', views.IndexView.as_view()),
    url('^brand/(?P<brand_id>\w+)/$', views.BrandPageView.as_view()),
    url('^brand/(?P<brand_id>\w+)/(?P<car_id>\w+)/$', views.CarPageView.as_view()),
    url('^filter/$', views.BrandPageView.get),
    url('^admin/', admin.site.urls),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [url(r'^__debug__/', include(debug_toolbar.urls))] + urlpatterns
