from django.conf.urls import patterns, url, include
from django.views.generic import TemplateView
# from osgeo_importer.urls import urlpatterns as importer_urlpatterns

# from geonode.urls import *

urlpatterns = patterns('',
   url(r'^/?$',
       TemplateView.as_view(template_name='site_index.html'),
       name='home'),
   )
#  + urlpatterns + [
#    #url(r'^chart/', include('charts_app.urls')),
#    #url(r'^table/', include('wfs_harvest.urls'))
#    ]

# urlpatterns += importer_urlpatterns
# avatar_patterns = [
#     url(r'^avatar/', include('avatar.urls')),
# ]

dummy_patterns = patterns(
    url(r'^/home?$',
       TemplateView.as_view(template_name='dummy_index.html'),
       name='layer_browse'),
    )

urlpatterns = urlpatterns + dummy_patterns
