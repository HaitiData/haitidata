__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '13/09/17'
# -*- coding: utf-8 -*-
"""Settings for when running under docker in development mode."""

import os
from .utils import ensure_secret_key_file

DEBUG = True
ensure_secret_key_file()

from .dev import *  # noqa

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'gis',
        'USER': 'docker',
        'PASSWORD': 'docker',
        'HOST': 'db',
        'PORT': 5432,
        'TEST_NAME': 'unittests',
    }
}

print INSTALLED_APPS
