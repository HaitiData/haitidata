from django.conf import settings  # import the settings file


def project_setting(request):
    return {'GEOSERVER_BASE_URL': settings.GEOSERVER_BASE_URL}
