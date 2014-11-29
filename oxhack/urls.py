from django.conf.urls import patterns, include, url
from django.contrib import admin
from oxhack import views


urlpatterns = patterns('',
    url(r'^$', 'oxhack.views.home', name='home'),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^inbound', views.inbound, name='inbound'),

    (r'^accounts/', include('registration.backends.default.urls')),
    (r'^accounts/', include('registration.auth_urls')),
    (r'^accounts/profile', views.home),
)
