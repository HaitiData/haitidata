# -*- coding: utf-8 -*-
#########################################################################
#
# Copyright (C) 2012 OpenPlans
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#########################################################################

# Django settings for the GeoNode project.
import os
from geonode.settings import *
#
# General Django development settings
#

SITENAME = 'haitidata'

# Defines the directory that contains the settings file as the LOCAL_ROOT
# It is used for relative settings elsewhere.
LOCAL_ROOT = os.path.abspath(os.path.dirname(__file__))

WSGI_APPLICATION = "haitidata.wsgi.application"


# Load more settings from a file called local_settings.py if it exists
try:
    from local_settings import *
except ImportError:
    pass

# Additional directories which hold static files
STATICFILES_DIRS.append(
    os.path.join(LOCAL_ROOT, "static"),
)

# Location of url mappings
ROOT_URLCONF = 'haitidata.urls'

# Location of locale files
LOCALE_PATHS = (
    os.path.join(LOCAL_ROOT, 'locale'),
    ) + LOCALE_PATHS

INSTALLED_APPS = INSTALLED_APPS + ('haitidata', 'osgeo_importer', 'geonode-client', 'charts_app', 'wfs_harvest')

LAYER_PREVIEW_LIBRARY = 'react'

TEMPLATES[0]['DIRS'].insert(0, os.path.join(LOCAL_ROOT, "templates"))

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

LOGGING['loggers']['osgeo_importer'] = {"handlers": ["console"], "level": "DEBUG"}
#DATABASE_ROUTERS = ['{{app_name}}.dbrouters.DefaultOnlyMigrations']

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

#import pyproj
#PROJECTION_DIRECTORY = os.path.join(os.path.dirname(pyproj.__file__), 'data/')
PROJECTION_DIRECTORY = '/tmp/'

try:
    CELERY_IMPORTS = CELERY_IMPORTS + ('osgeo_importer.tasks',)
except:
    CELERY_IMPORTS = ('osgeo_importer.tasks',)

LOCKDOWN_GEONODE = True

BROKER_URL = "amqp://guest@localhost:5672"
CELERY_ALWAYS_EAGER = True
IMPORT_TASK_SOFT_TIME_LIMIT = 90

MAX_CSV_RECORDS = 20000
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

SOCIAL_ORIGINS = [{
    "label":"paper-plane-o",
    "url":"mailto:?subject={name}&body={url}",
    "css_class":"email"
}, {
    "label":"facebook",
    "url":"http://www.facebook.com/sharer.php?u={url}",
    "css_class":"fb"
}, {
    "label":"twitter",
    "url":"https://twitter.com/share?url={url}&hashtags={hashtags}",
    "css_class":"tw"
}, {
    "label":"google-plus",
    "url":"https://plus.google.com/share?url={url}",
    "css_class":"gp"
}]
