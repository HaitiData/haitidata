from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.get_wfs_csv),
    url(r'^fields$', views.get_fields)
    ]
