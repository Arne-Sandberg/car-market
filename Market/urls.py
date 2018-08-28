from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from registration.backends.simple.views import RegistrationView

from MarketApp import views, api_views
from MarketApp.forms import UserCreateForm

urlpatterns = [
                  url('^accounts/register/$', views.CustomUserRegistration.as_view(form_class=UserCreateForm),
                      name='register'),
                  url('^accounts/', include('django.contrib.auth.urls')),
                  url('^accounts/profile/(?P<username>\w+)/$', views.ProfileView.as_view(), name='profile'),
                  url('^accounts/profile/settings/profile/$', views.EditProfileView.as_view, name='edit_profile'),
                  url('^accounts/profile/settings/password/$', views.EditPasswordView.as_view(), name='edit_password'),
                  url('^accounts/profile/settings/create_car/$', views.CreateCarView.as_view(), name='create_car'),
                  url('^accounts/profile/settings/edit_car/(?P<car_id>\d+)/$', views.EditCarView.as_view(),
                      name='edit_car'),
                  url('^accounts/profile/settings/connect_stripe/$', views.StripeConnectView.as_view(),
                      name='connect_stripe'),

                  url('^brand/(?P<brand_id>\d+)/$', views.BrandView.as_view(), name='brand'),
                  url('^brand/(?P<brand_id>\d+)/(?P<pk>\d+)/$', views.CarView.as_view(), name='car'),
                  url('^brand/(?P<brand_id>\d+)/(?P<pk>\d+)/checkout/$', views.CheckoutView.as_view(), name='checkout'),
                  url('^brand/(?P<brand_id>\d+)/(?P<pk>\d+)/checkout/(?P<flag>\w+)/$',
                      views.CheckoutResultView.as_view(),
                      name='checkout_result'),

                  url('^filter/(?P<filter_flag>\w+)/(?P<brand_id>\d+)/', views.BrandContent.as_view(), name='filter'),

                  url('^search/$', views.SearchView.as_view(), name='search'),

                  url('^comment/$', views.CommentContent.as_view(), name='comment'),

                  url('^delete/car/$', views.DeleteCarView.as_view(), name='delete_car'),

                  url('^home$|^$', views.IndexView.as_view(), name='home'),

                  url('^admin/', include(admin.site.urls)),

                  url(r'^api/v1/', include('rest_framework.urls')),
                  url(r'^api/v1/advertisement/', api_views.AdvertisementList.as_view()),
                  url(r'^api/v1/cars/$', api_views.CarList.as_view()),
                  url(r'^api/v1/cars/(?P<pk>\d+)/$', api_views.CarDetail.as_view(), name='car-detail'),
                  url(r'^api/v1/users/$', api_views.UserList.as_view()),
                  url(r'^api/v1/users/(?P<pk>\d+)/$', api_views.UserDetail.as_view(), name='user-detail'),
                  url(r'^api/v1/me/$', api_views.MyDetail.as_view()),
                  url(r'^api/v1/comments/$', api_views.CommentList.as_view()),
                  url(r'^api/v1/comments/(?P<pk>\d+)/$', api_views.CommentDetail.as_view(), name='comment-detail'),
                  url(r'^api/v1/purchases/$', api_views.PurchaseList.as_view()),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [url(r'^__debug__/', include(debug_toolbar.urls))] + urlpatterns
