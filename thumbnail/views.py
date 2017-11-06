from django.shortcuts import render

import base64

from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from geonode.layers.views import _resolve_layer
try:
    import json
except ImportError:
    from django.utils import simplejson as json

if 'geonode.geoserver' in settings.INSTALLED_APPS:
    from geonode.geoserver.helpers import _render_thumbnail


def layer_thumbnail(request, layername):
    if request.method == 'POST':
        layer_obj = _resolve_layer(request, layername)
        try:
            preview = json.loads(request.body).get('preview', None)
            if preview and preview == 'react':
                format, image = json.loads(
                    request.body)['image'].split(';base64,')
                image = base64.b64decode(image)
            else:
                image = _render_thumbnail(request.body)

            if not image:
                return
            filename = "layer-%s-thumb.png" % layer_obj.uuid
            layer_obj.save_thumbnail(filename, image)

            return HttpResponse('Thumbnail saved')
        except:
            return HttpResponse(
                content='error saving thumbnail',
                status=500,
                content_type='text/plain'
            )
