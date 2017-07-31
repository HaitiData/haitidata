from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns
from django.views.generic import TemplateView

admin.autodiscover()

urlpatterns = i18n_patterns(
    '',
    ("^admin/", include(admin.site.urls)),

    url("/home", TemplateView.as_view(template_name="dummy_index.html"), name="layer_browse"),
    url("/home/test", TemplateView.as_view(template_name="site_index.html"), name="home"),
)
