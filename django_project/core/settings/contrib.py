# coding=utf-8
"""
core.settings.contrib
"""
from .base import *  # noqa

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
