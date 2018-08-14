from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from registration.backends.simple.views import RegistrationView

from MarketApp import views
from MarketApp.forms import UserCreateForm

urlpatterns = [
    url('^accounts/register/$', RegistrationView.as_view(form_class=UserCreateForm)),
    url('^accounts/', include('registration.backends.simple.urls')),
    url('^accounts/profile/$', views.ProfileView.as_view()),
    url('^accounts/profile/edit/profile/$', views.EditProfileView.as_view()),
    url('^accounts/profile/edit/password/$', views.EditPasswordView.as_view()),
    url('^home$|^$', views.IndexView.as_view()),
    url('^brand/(?P<brand_id>\d+)/$', views.BrandView.as_view()),
    url('^brand/(?P<brand_id>\d+)/(?P<pk>\d+)/$', views.CarView.as_view()),
    url('^filter/(?P<brand_id>\d+)/', views.BrandContent.as_view()),
    url('^comment/$', views.CommentView.as_view()),
    url('^comment/edit/$', views.UserCommentView.as_view()),
    url('^brand/(?P<brand_id>\d+)/(?P<pk>\d+)/checkout/$', views.CheckoutView.as_view()),
    url('^brand/(?P<brand_id>\d+)/(?P<pk>\d+)/checkout/thanks/$', views.ThanksView.as_view()),
    url('^brand/(?P<brand_id>\d+)/(?P<pk>\d+)/checkout/error/$', views.ErrorView.as_view()),
    url('^admin/', admin.site.urls),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [url(r'^__debug__/', include(debug_toolbar.urls))] + urlpatterns
