# coding=utf-8
"""
core.settings.contrib
"""
from .base import *  # noqa
from distutils.util import strtobool
import os

# Store these package names here as they may change in the future since
# at the moment we are using custom forks of them.
PACKAGE_NAME_FILEBROWSER = "filebrowser_safe"
PACKAGE_NAME_GRAPPELLI = "grappelli_safe"
GRAPPELLI_INSTALLED = True

# Extra installed apps - grapelli needs to be added before others
INSTALLED_APPS += (
    "django_comments",
    "compressor",
    "avatar",
    "osgeo_importer",
    'pagination',
    'taggit',
    'treebeard',
    'friendlytagloader',
    'geoexplorer',
    'leaflet',
    'django_extensions',
    'autocomplete_light',
    'mptt',
    'djcelery',
    'storages',
    'geonode-client',

    # Theme
    "pinax_theme_bootstrap_account",
    "pinax_theme_bootstrap",
    'django_forms_bootstrap',

    # Social
    'account',
    'dialogos',
    'agon_ratings',
    # 'notification',
    'announcements',
    'actstream',
    'user_messages',
    'tastypie',
    'polymorphic',
    'guardian',
    'oauth2_provider',

# GeoNode internal apps
    'geonode',
    'geonode.base',
    'geonode.maps',
    'geonode.people',
    'geonode.layers',
    'geonode.proxy',
    'geonode.security',
    'geonode.social',
    'geonode.catalogue',
    'geonode.documents',
    'geonode.api',
    'geonode.groups',
    'geonode.services',

    # QGIS Server Apps
    # 'geonode_qgis_server',

    # GeoServer Apps
    # Geoserver needs to come last because
    # it's signals may rely on other apps' signals.
    'geonode.geoserver',
    'geonode.upload',
    'geonode.tasks',

)

MARKDOWNIFY_WHITELIST_TAGS = [
    'a',
    'abbr',
    'acronym',
    'b',
    'blockquote',
    'em',
    'i',
    'li',
    'ol',
    'p',
    'strong',
    'ul'
]

ACCOUNT_OPEN_SIGNUP = True
ACCOUNT_EMAIL_UNIQUE = True
ACCOUNT_EMAIL_CONFIRMATION_REQUIRED = False
ACCOUNT_SIGNUP_REDIRECT_URL = "dashboard"
ACCOUNT_LOGIN_REDIRECT_URL = "dashboard"
ACCOUNT_LOGOUT_REDIRECT_URL = "home"
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 2
ACCOUNT_USE_AUTH_AUTHENTICATE = True
HOOKSET = "pinaxcon_theme.hooks.Foss4GAccountHookset"
MODIFY_TOPICCATEGORY = False
EXTRA_LANG_INFO = []


DEFAULT_WORKSPACE = os.getenv('DEFAULT_WORKSPACE', 'geonode')
CASCADE_WORKSPACE = os.getenv('CASCADE_WORKSPACE', 'geonode')
OGP_URL = os.getenv('OGP_URL', "http://geodata.tufts.edu/solr/select")


MISSING_THUMBNAIL = os.getenv(
    'MISSING_THUMBNAIL', 'geonode/img/missing_thumb.png'
)

# Search Snippet Cache Time in Seconds
CACHE_TIME = int(os.getenv('CACHE_TIME', '0'))

AUTH_USER_MODEL = os.getenv('AUTH_USER_MODEL', 'people.Profile')

GEOSERVER_LOCATION = 'http://geoserver:8080/geoserver/'
GEOSERVER_PUBLIC_LOCATION = os.environ.get('GEOSERVER_PUBLIC_LOCATION','http://0.0.0.0:33300/api/geoserver/')

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
        'USER': 'admin',
        'PASSWORD': 'geoserver',
        'MAPFISH_PRINT_ENABLED': True,
        'PRINT_NG_ENABLED': True,
        'GEONODE_SECURITY_ENABLED': True,
        'GEOGIG_ENABLED': False,
        'WMST_ENABLED': False,
        'BACKEND_WRITE_ENABLED': True,
        'WPS_ENABLED': False,
        # Set to name of database in DATABASES dictionary to enable
        'DATASTORE': '',  # 'datastore',
        'PG_GEOGIG': False,
        'TIMEOUT': 10  # number of seconds to allow for HTTP requests
    }
}

ALLOWED_DOCUMENT_TYPES = ["pdf"]
MISSING_THUMBNAIL = os.getenv(
    'MISSING_THUMBNAIL', 'geonode/img/missing_thumb.png'
)
# Whether the uplaoded resources should be public and downloadable by default
# or not
DEFAULT_ANONYMOUS_VIEW_PERMISSION = strtobool(
    os.getenv('DEFAULT_ANONYMOUS_VIEW_PERMISSION', 'True')
)
DEFAULT_ANONYMOUS_DOWNLOAD_PERMISSION = strtobool(
    os.getenv('DEFAULT_ANONYMOUS_VIEW_PERMISSION', 'True')
)

# Available download formats
DOWNLOAD_FORMATS_METADATA = [
    'Atom', 'DIF', 'Dublin Core', 'ebRIM', 'FGDC', 'ISO',
]
DOWNLOAD_FORMATS_VECTOR = [
    'JPEG', 'PDF', 'PNG', 'Zipped Shapefile', 'GML 2.0', 'GML 3.1.1', 'CSV',
    'Excel', 'GeoJSON', 'KML', 'View in Google Earth', 'Tiles',
]
DOWNLOAD_FORMATS_RASTER = [
    'JPEG',
    'PDF',
    'PNG',
    'ArcGrid',
    'GeoTIFF',
    'Gtopo30',
    'ImageMosaic',
    'KML',
    'View in Google Earth',
    'Tiles',
    'GML',
    'GZIP'
]

API_INCLUDE_REGIONS_COUNT = False
HAYSTACK_SEARCH = False
RESOURCE_PUBLISHING = True
SITEURL = os.getenv('SITEURL', "http://localhost:33300/")

# Uploader Settings
UPLOADER = {
    'BACKEND': 'geonode.rest',
    'OPTIONS': {
        'TIME_ENABLED': False,
        'MOSAIC_ENABLED': False,
        'GEOGIG_ENABLED': False,
    }
}

# CSW settings
CATALOGUE = {
    'default': {
        # The underlying CSW implementation
        # default is pycsw in local mode (tied directly to GeoNode Django DB)
        'ENGINE': 'geonode.catalogue.backends.pycsw_local',
        # pycsw in non-local mode
        # 'ENGINE': 'geonode.catalogue.backends.pycsw_http',
        # GeoNetwork opensource
        # 'ENGINE': 'geonode.catalogue.backends.geonetwork',
        # deegree and others
        # 'ENGINE': 'geonode.catalogue.backends.generic',

        # The FULLY QUALIFIED base url to the CSW instance for this GeoNode
        'URL': '%scatalogue/csw' % SITEURL,
        # 'URL': 'http://localhost:8080/geonetwork/srv/en/csw',
        # 'URL': 'http://localhost:8080/deegree-csw-demo-3.0.4/services',

        # login credentials (for GeoNetwork)
        # 'USER': 'admin',
        # 'PASSWORD': 'admin',
    }
}

# pycsw settings
PYCSW = {
    # pycsw configuration
    'CONFIGURATION': {
        # uncomment / adjust to override server config system defaults
        # 'server': {
        #    'maxrecords': '10',
        #    'pretty_print': 'true',
        #    'federatedcatalogues': 'http://catalog.data.gov/csw'
        # },
        'metadata:main': {
            'identification_title': 'GeoNode Catalogue',
            'identification_abstract': 'GeoNode is an open source platform' \
                                       ' that facilitates the creation, sharing, and collaborative use' \
                                       ' of geospatial data',
            'identification_keywords': 'sdi, catalogue, discovery, metadata,' \
                                       ' GeoNode',
            'identification_keywords_type': 'theme',
            'identification_fees': 'None',
            'identification_accessconstraints': 'None',
            'provider_name': 'Organization Name',
            'provider_url': SITEURL,
            'contact_name': 'Lastname, Firstname',
            'contact_position': 'Position Title',
            'contact_address': 'Mailing Address',
            'contact_city': 'City',
            'contact_stateorprovince': 'Administrative Area',
            'contact_postalcode': 'Zip or Postal Code',
            'contact_country': 'Country',
            'contact_phone': '+xx-xxx-xxx-xxxx',
            'contact_fax': '+xx-xxx-xxx-xxxx',
            'contact_email': 'Email Address',
            'contact_url': 'Contact URL',
            'contact_hours': 'Hours of Service',
            'contact_instructions': 'During hours of service. Off on ' \
                                    'weekends.',
            'contact_role': 'pointOfContact',
        },
        'metadata:inspire': {
            'enabled': 'true',
            'languages_supported': 'eng,gre',
            'default_language': 'eng',
            'date': 'YYYY-MM-DD',
            'gemet_keywords': 'Utility and governmental services',
            'conformity_service': 'notEvaluated',
            'contact_name': 'Organization Name',
            'contact_email': 'Email Address',
            'temp_extent': 'YYYY-MM-DD/YYYY-MM-DD',
        }
    }
}

# GeoNode javascript client configuration

# default map projection
# Note: If set to EPSG:4326, then only EPSG:4326 basemaps will work.
DEFAULT_MAP_CRS = "EPSG:900913"

# Where should newly created maps be focused?
DEFAULT_MAP_CENTER = (0, 0)

# How tightly zoomed should newly created maps be?
# 0 = entire world;
# maximum zoom is between 12 and 15 (for Google Maps, coverage varies by area)
DEFAULT_MAP_ZOOM = 0

ALT_OSM_BASEMAPS = os.environ.get('ALT_OSM_BASEMAPS', False)
CARTODB_BASEMAPS = os.environ.get('CARTODB_BASEMAPS', False)
STAMEN_BASEMAPS = os.environ.get('STAMEN_BASEMAPS', False)
THUNDERFOREST_BASEMAPS = os.environ.get('THUNDERFOREST_BASEMAPS', False)
MAPBOX_ACCESS_TOKEN = os.environ.get('MAPBOX_ACCESS_TOKEN', None)
BING_API_KEY = os.environ.get('BING_API_KEY', None)
CLIENT_RESULTS_LIMIT = 10
REGISTRATION_OPEN = False
THEME_ACCOUNT_CONTACT_EMAIL = "anis@kartoza.com"

MAP_BASELAYERS = [{
    "source": {"ptype": "gxp_olsource", "url": GEOSERVER_PUBLIC_LOCATION + "wms"},
    "type": "OpenLayers.Layer",
    "args": ["No background"],
    "name": "background",
    "visibility": False,
    "fixed": True,
    "group": "background"
}, {
    "source": {"ptype": "gxp_osmsource"},
    "type": "OpenLayers.Layer.OSM",
    "name": "mapnik",
    "visibility": True,
    "fixed": True,
    "group": "background"
}]