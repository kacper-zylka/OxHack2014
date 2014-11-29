from django.conf.urls import patterns, include, url
from django.contrib import admin
from oxhack import views


urlpatterns = patterns('',
    url(r'^$', 'oxhack.views.home', name='home'),

    url(r'^rules$', 'oxhack.views.rules', name='rules'),
    url(r'^leaderboard$', 'oxhack.views.leaderboard', name='leaderboard'),
    url(r'^visualisations$', 'oxhack.views.visualisations', name='visualisations'),
    url(r'^about$', 'oxhack.views.about', name='about'),
    url(r'^register$', 'oxhack.views.register', name='register'),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^inbound', views.inbound, name='inbound'),
)
