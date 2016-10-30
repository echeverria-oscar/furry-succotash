from django.conf.urls import url, include
from . import views


urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^quotes$', views.quotes),
    url(r'^add_qoute$', views.add_qoute),
    url(r'^profile/(?P<id>\d+)$', views.profile),
    url(r'^add_favorites/(?P<id>\d+)$', views.add_favorites),
    url(r'^remove_favorites/(?P<id>\d+)$', views.remove_favorites),
]
