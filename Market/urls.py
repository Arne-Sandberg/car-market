from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from MarketApp import views

urlpatterns = [
    url('^accounts/', include('registration.backends.simple.urls')),
    url('^home$|^$', views.IndexView.as_view()),
    url('^brand/(?P<brand_id>\d+)/$', views.BrandPageView.as_view()),
    url('^brand/(?P<brand_id>\d+)/(?P<pk>\d+)/$', views.CarPageView.as_view()),
    url('^filter/(?P<brand_id>\d+)/', views.BrandContent.as_view()),
    url('^admin/', admin.site.urls),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [url(r'^__debug__/', include(debug_toolbar.urls))] + urlpatterns
