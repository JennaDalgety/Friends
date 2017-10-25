from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^friends$', views.friends),
    url(r'^user/(?P<id>\d+)$', views.show),
    url(r'^add_friend$', views.add_friend),
    url(r'^clear$', views.clear),
    url(r'^destroy/(?P<id>\d+)$', views.destroy)
]