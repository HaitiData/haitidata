import os
from .secret import *
from geonode.settings import *  # Django settings for the GeoNode project.
from .utils import absolute_path

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Africa/Johannesburg'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# The numeric mode to set newly-uploaded files to. The value should be
# a mode you'd pass directly to os.chmod.
FILE_UPLOAD_PERMISSIONS = 0o644

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = '/home/web/media'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
# MEDIA_URL = '/media/'
# setting full MEDIA_URL to be able to use it for the feeds
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = '/home/web/static'

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

SYMPOSION_STATIC_URL = "/site_media/"

# Additional locations of static files
STATICFILES_DIRS += (
    absolute_path('core', 'base_static'),
    absolute_path('core', 'geonode_static'),
)

# Additional locations of static files

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# import SECRET_KEY into current namespace
# noinspection PyUnresolvedReferences
from .secret import SECRET_KEY  # noqa

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    "django.template.loaders.filesystem.Loader",
    "django.template.loaders.app_directories.Loader",
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            # project level templates
            absolute_path('core', 'templates'),
        ],
        'APP_DIRS': False,
        'OPTIONS': {
            #  List of callables that know how to import
            #  templates from various sources.
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
            'context_processors': [
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.core.context_processors.debug",
                "django.core.context_processors.i18n",
                "django.core.context_processors.static",
                "django.core.context_processors.media",
                "django.core.context_processors.request",
                "django.core.context_processors.tz",
                'account.context_processors.account',
                'geonode.context_processors.resource_urls',
                "geonode.geoserver.context_processors.geoserver_urls",
                "core.context_processors.project_setting.project_setting",
            ],
        },
    },
]

ROOT_URLCONF = 'core.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'core.wsgi.application'

SITENAME = 'haitidata'

# Defines the directory that contains the settings file as the LOCAL_ROOT
# It is used for relative settings elsewhere.
LOCAL_ROOT = os.path.abspath(os.path.dirname(__file__))
LOCAL_MEDIA_URL = LOCAL_ROOT
AVATAR_PATH_HANDLER = LOCAL_ROOT
LAYER_PREVIEW_LIBRARY = 'react'

IMPORT_HANDLERS = [
    # If GeoServer handlers are enabled, you must have an instance of geoserver running.
    # Warning: the order of the handlers here matters.
    'osgeo_importer.handlers.FieldConverterHandler',
    'osgeo_importer.handlers.geoserver.GeoserverPublishHandler',
    'osgeo_importer.handlers.geoserver.GeoserverPublishCoverageHandler',
    'osgeo_importer.handlers.geoserver.GeoServerTimeHandler',
    'osgeo_importer.handlers.geoserver.GeoWebCacheHandler',
    'osgeo_importer.handlers.geoserver.GeoServerBoundsHandler',
    'osgeo_importer.handlers.geoserver.GenericSLDHandler',
    'osgeo_importer.handlers.geonode.GeoNodePublishHandler',
    'osgeo_importer.handlers.mapproxy.publish_handler.MapProxyGPKGTilePublishHandler',
    'osgeo_importer.handlers.geoserver.GeoServerStyleHandler',
    'osgeo_importer.handlers.geonode.GeoNodeMetadataHandler'
]

OSGEO_DATASTORE = 'datastore'
OSGEO_IMPORTER_GEONODE_ENABLED = True
OSGEO_IMPORTER_VALID_EXTENSIONS = [
    'shp', 'shx', 'prj', 'dbf', 'kml', 'geojson', 'json', 'tif', 'tiff',
    'gpkg', 'csv', 'zip', 'xml', 'sld'
]

# DATABASE_ROUTERS = ['{{app_name}}.dbrouters.DefaultOnlyMigrations']

# # === MapProxy settings
# # This is the location to place additional configuration files for mapproxy to work from.
# # Currently it is only to allow tiles from gpkg files to be served.
MAPPROXY_CONFIG_DIR = '/opt/geonode-mapproxy-config'
# Name of the mapproxy config file to create for tile gpkg files.
MAPPROXY_CONFIG_FILENAME = 'geonode.yaml'
# This is the base URL for MapProxy WMS services
# URLs will look like this: /geonode/tms/1.0.0/<layer_name>/<grid_name>/0/0/0.png and a <grid_name> will be
# set as '<layer_name>_<projection_id>' (by conf_from_geopackage()).
MAPPROXY_SERVER_LOCATION = 'http://localhost:8088/geonode/tms/1.0.0/{layer_name}/{grid_name}/'

# import pyproj
# PROJECTION_DIRECTORY = os.path.join(os.path.dirname(pyproj.__file__), 'data/')
PROJECTION_DIRECTORY = '/tmp/'

try:
    CELERY_IMPORTS = CELERY_IMPORTS + ('osgeo_importer.tasks',)
except:
    CELERY_IMPORTS = ('osgeo_importer.tasks',)

BROKER_URL = "amqp://guest@localhost:5672"
CELERY_ALWAYS_EAGER = True
IMPORT_TASK_SOFT_TIME_LIMIT = 90

MAX_CSV_RECORDS = 20000

DEBUG = True
