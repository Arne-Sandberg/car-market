from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from registration.backends.simple.views import RegistrationView

from MarketApp import views
from MarketApp.forms import UserCreateForm

urlpatterns = [
    url('^accounts/register/$', RegistrationView.as_view(form_class=UserCreateForm), name='register'),
    url('^accounts/', include('django.contrib.auth.urls')),
    url('^accounts/profile/(?P<username>\w+)/$', views.ProfileView.as_view(), name='profile'),
    url('^accounts/profile/settings/profile/$', views.EditProfileView.as_view(), name='edit_profile'),
    url('^accounts/profile/settings/password/$', views.EditPasswordView.as_view(), name='edit_password'),
    url('^accounts/profile/settings/create_car/$', views.CreateCarView.as_view(), name='create_car'),
    url('^accounts/profile/settings/edit_car/(?P<car_id>\d+)/$', views.EditCarView.as_view(), name='edit_car'),
    url('^delete/car/$', views.DeleteCarView.as_view(), name='delete_car'),

    url('^brand/(?P<brand_id>\d+)/$', views.BrandView.as_view(), name='brand'),
    url('^brand/(?P<brand_id>\d+)/(?P<pk>\d+)/$', views.CarView.as_view(), name='car'),
    url('^brand/(?P<brand_id>\d+)/(?P<pk>\d+)/checkout/$', views.CheckoutView.as_view(), name='checkout'),
    url('^brand/(?P<brand_id>\d+)/(?P<pk>\d+)/checkout/thanks/$', views.ThanksView.as_view(), name='thanks'),
    url('^brand/(?P<brand_id>\d+)/(?P<pk>\d+)/checkout/error/$', views.ErrorView.as_view(), name='error'),

    url('^filter/(?P<brand_id>\d+)/', views.BrandContent.as_view(), name='filter'),

    url('^comment/$', views.CommentContent.as_view(), name='comment'),
    # url('^comment/edit/$', views.CommentView.as_view(), name='edit_comment'),

    url('^home$|^$', views.IndexView.as_view(), name='home'),

    url('^admin/', include(admin.site.urls)),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [url(r'^__debug__/', include(debug_toolbar.urls))] + urlpatterns
