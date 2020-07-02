from os.path import basename, splitext
from os import walk
from django.conf import settings


def clipped_geotiff(request):
    geotiff_filename = []
    for (dirpath, dirnames, filenames) in walk(
            settings.CLIPPED_DIRECTORY):
        filenames = splitext(filenames[0])
        geotiff_filename.append(filenames[0])

    return {'CLIPPED_LAYERNAME': geotiff_filename}
