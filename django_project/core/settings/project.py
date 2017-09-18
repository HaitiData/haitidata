# -*- coding: utf-8 -*-

from .base import *
from django.utils.translation import ugettext_lazy as _

PROJECTION_DIRECTORY = '/tmp/'

GEOSERVER_BASE_URL = 'http://0.0.0.0:33308/geoserver/'
GEOSERVER_LOCATION = 'http://geoserver:8080/geoserver/'
GEOSERVER_PUBLIC_LOCATION = os.environ.get(
    'GEOSERVER_PUBLIC_LOCATION',
    'http://0.0.0.0:33300/api/geoserver/'
)

OGC_SERVER = {
    'default': {
        'BACKEND': 'geonode.geoserver',
        'LOCATION': GEOSERVER_LOCATION,
        'LOGIN_ENDPOINT': 'j_spring_oauth2_geonode_login',
        'LOGOUT_ENDPOINT': 'j_spring_oauth2_geonode_logout',
        # PUBLIC_LOCATION needs to be kept like this because in dev mode
        # the proxy won't work and the integration tests will fail
        # the entire block has to be overridden in the local_settings
        'PUBLIC_LOCATION': GEOSERVER_PUBLIC_LOCATION,
        'USER': OGC_SERVER_DEFAULT_USER,
        'PASSWORD': OGC_SERVER_DEFAULT_PASSWORD,
        'MAPFISH_PRINT_ENABLED': True,
        'PRINT_NG_ENABLED': True,
        'GEONODE_SECURITY_ENABLED': True,
        'GEOGIG_ENABLED': False,
        'WMST_ENABLED': False,
        'BACKEND_WRITE_ENABLED': True,
        'WPS_ENABLED': False,
        'LOG_FILE': '%s/geoserver/data/logs/geoserver.log'
                    % os.path.abspath(os.path.join(PROJECT_ROOT, os.pardir)),
        # Set to name of database in DATABASES dictionary to enable
        'DATASTORE': 'datastore',
        'PG_GEOGIG': False,
        'TIMEOUT': 10  # number of seconds to allow for HTTP requests
    }
}

# Project apps
INSTALLED_APPS += (
    "django.contrib.redirects",
    "osgeo_importer",
    'geonode-client',

    # Add any additional project apps here
    "charts_app",
    "wfs_harvest",
    "clip-and-ship"

)

# Set languages which want to be translated
LANGUAGES = (
    ('en', _('English')),
    ('fr', _('Francais')),
)

# Set storage path for the translation files
LOCALE_PATHS = (
    absolute_path('locale'),
)

DATABASES = {}

# default login url
LOGIN_URL = '/account/login/'

# maximum clip size in bytes
MAXIMUM_CLIP_SIZE = '40000000'

SOCIAL_ORIGINS = [{
    "label": "paper-plane-o",
    "url": "mailto:?subject={name}&body={url}",
    "css_class": "email"
}, {
    "label": "facebook",
    "url": "http://www.facebook.com/sharer.php?u={url}",
    "css_class": "fb"
}, {
    "label": "twitter",
    "url": "https://twitter.com/share?url={url}&hashtags={hashtags}",
    "css_class": "tw"
}, {
    "label": "google-plus",
    "url": "https://plus.google.com/share?url={url}",
    "css_class": "gp"
}]
