from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns
from django.views.generic import TemplateView
from geonode.sitemap import LayerSitemap, MapSitemap
from geonode.api.urls import api
from geonode.api.views import verify_token, roles, users, admin_role

import autocomplete_light

autocomplete_light.autodiscover()
admin.autodiscover()

js_info_dict = {
    'domain': 'djangojs',
    'packages': ('geonode',)
}

sitemaps = {
    "layer": LayerSitemap,
    "map": MapSitemap
}
from osgeo_importer.urls import urlpatterns as importer_urlpatterns

from geonode.urls import *

urlpatterns = i18n_patterns(
    '',
    url(r'^/?$', TemplateView.as_view(template_name='site_index.html'), name='home'),
    url(r'^', include('geonode.urls')),
    url(r'^chart/', include('charts_app.urls')),
    url(r'^table/', include('wfs_harvest.urls'))
)

urlpatterns += importer_urlpatterns
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
