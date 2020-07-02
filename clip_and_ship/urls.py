from django.conf.urls import url

from . import views
from .views import ClipView

urlpatterns = [
    url(r'^(?P<geotiffname>[^/]*)$', ClipView.as_view(), name="clip_layer_page"),
    url(r'^(?P<layername>[^/]*)/clip-layer$', views.clip_layer, name="clip_layer"),
    url(r'^(?P<layername>[^/]*)/(?P<clip_filename>[^/]*)/download-clip$', views.download_clip, name="download_clip"),
]
