from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from MarketApp import views

urlpatterns = [
    url('^accounts/', include('registration.backends.simple.urls')),
    url('^accounts/profile/$', views.ProfileView.as_view()),
    url('^accounts/profile/edit/$', views.EditView.as_view()),
    url('^home$|^$', views.IndexView.as_view()),
    url('^brand/(?P<brand_id>\d+)/$', views.BrandView.as_view()),
    url('^brand/(?P<brand_id>\d+)/(?P<pk>\d+)/$', views.CarView.as_view()),
    url('^filter/(?P<brand_id>\d+)/', views.BrandContent.as_view()),
    url('^brand/(?P<brand_id>\d+)/(?P<pk>\d+)/checkout/$', views.CheckoutView.as_view()),
    url('^brand/(?P<brand_id>\d+)/(?P<pk>\d+)/checkout/thanks/$', views.ThanksView.as_view()),
    url('^brand/(?P<brand_id>\d+)/(?P<pk>\d+)/checkout/error/$', views.ErrorView.as_view()),
    url('^admin/', admin.site.urls),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [url(r'^__debug__/', include(debug_toolbar.urls))] + urlpatterns
