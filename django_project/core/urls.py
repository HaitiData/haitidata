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

urlpatterns = i18n_patterns(
    url(r'^home', TemplateView.as_view(template_name="dummy_index.html"), name="layer_browse"),
    url(r'^help/$', TemplateView.as_view(template_name='help.html'), name='help'),
    url(r'^developer/$', TemplateView.as_view(template_name='developer.html'), name='developer'),
    url(r'^about/$', TemplateView.as_view(template_name='about.html'), name='about'),
    url(r'^api/home/test', TemplateView.as_view(template_name="site_index.html"), name="home"),
    url(r'^chart/', include('charts_app.urls')),
    url(r'^table/', include('wfs_harvest.urls')),
    url(r'^layers/', include('geonode.layers.urls')),

    # Map views
    url(r'^maps/', include('geonode.maps.urls')),

    # Catalogue views
    url(r'^catalogue/', include('geonode.catalogue.urls')),

    # data.json
    url(r'^data.json$', 'geonode.catalogue.views.data_json', name='data_json'),

    # ident
    url(r'^ident.json$', 'geonode.views.ident_json', name='ident_json'),

    # h keywords
    url(r'^h_keywords_api$', 'geonode.views.h_keywords', name='h_keywords_api'),

    # Search views
    url(r'^search/$', TemplateView.as_view(template_name='search/search.html'), name='search'),

    # Social views
    url(r"^account/", include("account.urls")),
    url(r'^people/', include('geonode.people.urls')),
    url(r'^avatar/', include('avatar.urls')),
    url(r'^comments/', include('dialogos.urls')),
    url(r'^ratings/', include('agon_ratings.urls')),
    url(r'^activity/', include('actstream.urls')),
    url(r'^announcements/', include('announcements.urls')),
    url(r'^messages/', include('user_messages.urls')),
    url(r'^social/', include('geonode.social.urls')),
    url(r'^security/', include('geonode.security.urls')),

    # Accounts
    url(r'^account/ajax_login$', 'geonode.views.ajax_login', name='account_ajax_login'),
    url(r'^account/ajax_lookup$', 'geonode.views.ajax_lookup', name='account_ajax_lookup'),

    # Meta
    url(r'^lang\.js$', TemplateView.as_view(template_name='lang.js', content_type='text/javascript'),
        name='lang'),

    url(r'^jsi18n/$', 'django.views.i18n.javascript_catalog', js_info_dict, name='jscat'),
    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps},
        name='sitemap'),

    url(r'^autocomplete/', include('autocomplete_light.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^groups/', include('geonode.groups.urls')),
    url(r'^documents/', include('geonode.documents.urls')),
    url(r'^services/', include('geonode.services.urls')),
    # OAuth Provider
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),

    # Api Views
    url(r'^api/o/v4/tokeninfo', verify_token, name='tokeninfo'),
    url(r'^api/roles', roles, name='roles'),
    url(r'^api/adminRole', admin_role, name='adminRole'),
    url(r'^api/users', users, name='users'),
    url(r'', include(api.urls)),
)
