from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns
from django.views.generic import TemplateView

admin.autodiscover()

urlpatterns = i18n_patterns(
    url("^admin/", include(admin.site.urls)),
    url(r'^home', TemplateView.as_view(template_name="dummy_index.html"), name="layer_browse"),
    url(r'^api/home/test', TemplateView.as_view(template_name="site_index.html"), name="home"),
    url(r'^chart/', include('charts_app.urls')),
    url(r'^table/', include('wfs_harvest.urls')),
    url(r'^geonode/document/', include('geonode.documents.urls')),
    url(r'^geonode/maps/', include('geonode.maps.urls')),
    url(r'^geonode/people/', include('geonode.people.urls')),
    url(r'^geonode/groups/', include('geonode.groups.urls')),
    url(r'^geonode/', include('geonode.urls')),
)
