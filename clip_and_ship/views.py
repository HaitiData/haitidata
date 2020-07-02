# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import os
import tempfile
import StringIO
import zipfile
import urllib2

import subprocess

from pyproj import Proj, transform
from django.conf import settings
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic.detail import View
from geonode.layers.views import _resolve_layer, _PERMISSION_MSG_VIEW
from geonode.layers.models import Layer

WCS_URL = settings.GEOSERVER_PUBLIC_LOCATION + \
          'wcs?request=getcoverage&' \
          'version=1.0.0&service=WCS&coverage={layer_name}&' \
          'format=geotiff&crs=EPSG:4326&bbox={bbox}&width={width}&' \
          'height={height}'

WCS_URL_2_0_1 = settings.GEOSERVER_PUBLIC_LOCATION + \
                'wcs?request=getcoverage&' \
                'version=2.0.1&service=WCS&coverageid={layer_name}&' \
                'format=geotiff&crs=EPSG:4326&subset=E({x1},{x2})&subset=N({y1},{y2})'

WCS_URL_dev = settings.GEOSERVER_PUBLIC_LOCATION + \
          'wcs?request=getcoverage&' \
          'version=1.0.0&service=WCS&coverage={layer_name}&' \
          'format=geotiff&crs=EPSG:4326&bbox={bbox}&width={width}&' \
          'height={height}'

WCS_URL_2_0_1_dev = settings.GEOSERVER_PUBLIC_LOCATION + \
                'wcs?request=getcoverage&' \
                'version=2.0.1&service=WCS&coverageid={layer_name}&' \
                'format=geotiff&crs=EPSG:4326&subset=E({x1},{x2})&subset=N({y1},{y2})'

MAX_CLIP_SIZE = settings.MAXIMUM_CLIP_SIZE
TILE_SAMPLE_SIZE = 100  # tile sample size will be 100*100


def check_file_size(clipped_size):
    """ Checking file size that is allowed or not

    :param clipped_size: File size to be checked
    :type clipped_size: float

    :return: Checking file size is allowed or not
    :rtype: bool
    """
    if float(clipped_size) > float(MAX_CLIP_SIZE):
        return False
    return True


def download_wcs(layername, bbox_string, width, height, raster_filepath):
    """ Download clipped image from wcs.

    :param layername: layername for wcs request
    :type layername: str

    :param bbox_string: bbox string for wcs request
    :type bbox_string: str

    :param width: width for wcs request
    :type width: int

    :param height: height for wcs request
    :type height: int

    :param raster_filepath: filepath for downloaded wcs clipped
    :type raster_filepath: str

    :return:
    """
    if layername == 'geonode:ortho_images' or layername == 'geonode:lidar':
        wcs_formatted_url = WCS_URL_dev.format(
            layer_name=layername,
            bbox=bbox_string,
            width=width,
            height=height
        )
    else:
        wcs_formatted_url = WCS_URL.format(
            layer_name=layername,
            bbox=bbox_string,
            width=width,
            height=height
        )

    response = urllib2.urlopen(wcs_formatted_url)
    fh = open(raster_filepath, "w")
    fh.write(response.read())
    fh.close()


def download_wcs_v2(layername, x1, x2, y1, y2, raster_filepath):
    """ Download clipped image from wcs.

    :param raster_filepath: filepath for downloaded wcs clipped
    :type raster_filepath: str

    :return:
    """
    if layername == 'geonode:ortho_images' or layername == 'geonode:lidar':
        wcs_formatted_url = WCS_URL_2_0_1_dev.format(
            layer_name=layername,
            x1=x1,
            x2=x2,
            y1=y1,
            y2=y2
        )
    else:
        wcs_formatted_url = WCS_URL_2_0_1.format(
            layer_name=layername,
            x1=x1,
            x2=x2,
            y1=y1,
            y2=y2
        )

    response = urllib2.urlopen(wcs_formatted_url)
    fh = open(raster_filepath, "w")
    fh.write(response.read())
    fh.close()


def clip_layer(request, layername):
    """Clipping raster layer and save to temp folder.
    Clipping layer by bbox or by geojson.
    :param layername: The layer name in Geonode.
    :type layername: basestring
    :return: file size
    """
    # PREPARATION
    try:
        layer = Layer.objects.get(
                workspace=layername.split(':')[0],
                name=layername.split(':')[1]
        )
    except Http404 as e:
        response = JsonResponse({
            'error': '%s. '
                     'Please do '
                     '<i>python manage.py updatelayers</i> '
                     'to retrieve it from geoserver.' % e
        })
        response.status_code = 404
        return response

    download_from_wcs = False

    query = request.GET or request.POST
    params = {
        param.upper(): value for param, value in query.iteritems()}
    bbox_string = params.get('BBOX', '')
    geojson = params.get('GEOJSON', '')
    current_date = datetime.datetime.today().strftime('%Y-%m-%d_%H-%M-%S')

    # create temp folder
    temporary_folder = os.path.join(
        tempfile.gettempdir(), 'clipped')
    try:
        os.mkdir(temporary_folder)
    except OSError as e:
        pass

    # get file for raster
    raster_filepath = None
    extention = ''

    # get file for raster
    try:
        if not raster_filepath:
            file_names = []
            for layerfile in layer.upload_session.layerfile_set.all():
                file_names.append(layerfile.file.path)

            for target_file in file_names:
                if '.tif' in target_file:
                    raster_filepath = target_file
                    extention = 'tif'
                    break
        bbox_array = bbox_string.split(',')
        southwest_lat = bbox_array[1]
        bbox_array[1] = bbox_array[3]
        bbox_array[3] = southwest_lat
        bbox_string = ','.join(bbox_array)
    except AttributeError:
        # Call wcs command
        bbox_array = bbox_string.split(',')
        offset = 50
        x = float(bbox_array[2]) - float(bbox_array[0])
        width = int(x * 43260) + offset

        y = float(bbox_array[3]) - float(bbox_array[1])
        height = int(y * 43260) + offset

        width = int(width * settings.WCS_DOWNLOADED_RATIO_SIZE)
        height = int(height * settings.WCS_DOWNLOADED_RATIO_SIZE)

        extention = 'tif'

        # checking file size of wcs download
        # it is done by assumption by getting sample
        # 1. getting part 10x10 through wcs
        # 2. get the filesize
        # 3. times filesize by width/10 * height/10, as assumption for actual filesize
        # -------------------------------------------------
        number_tile_in_width = int(width / TILE_SAMPLE_SIZE)
        number_tile_in_height = int(height / TILE_SAMPLE_SIZE)

        sample_filepath = os.path.join(
            temporary_folder,
            layer.title + '.sample.' + extention)
        download_wcs(
            layername, bbox_string,
            TILE_SAMPLE_SIZE,
            TILE_SAMPLE_SIZE,
            sample_filepath)

        expected_clip_size = os.path.getsize(sample_filepath)
        # size of 10x10 times width_sample * height_sample
        expected_clip_size = expected_clip_size * (
            number_tile_in_width * number_tile_in_height
        )

        if not check_file_size(expected_clip_size):
            response = JsonResponse({
                'error': 'Clipped file size is '
                         'bigger than %s mb' % (
                             int(MAX_CLIP_SIZE) / 1000000
                         )
            })
            response.status_code = 403
            return response

        # -------------------------------------------------

        # download actual wcs clipped
        raster_filepath = os.path.join(
            temporary_folder,
            layer.title + '.' + extention)
        x1, x2 = bbox_array[0], bbox_array[2]
        y1, y2 = bbox_array[1], bbox_array[3]
        inProj = Proj(init='epsg:4326')
        outProj = Proj(init='epsg:32618')

        x1, y1 = transform(inProj, outProj, x1, y1)
        x2, y2 = transform(inProj, outProj, x2, y2)

        download_wcs_v2(layername, x1, x2, y1, y2, raster_filepath)

        if not geojson:
            response = JsonResponse({
                'success': 'Successfully clipping layer',
                'clip_filename': os.path.basename(raster_filepath)
            })
            response.status_code = 200
            return response

        download_from_wcs = True

    # get temp filename for output
    filename = os.path.basename(raster_filepath)
    if len(filename.split('.')) >= 3:
        filename = filename.split('.')[0]
    clip_filename = filename + '.' + current_date + '.' + extention

    if bbox_string and not download_from_wcs and not geojson:
        output = os.path.join(
            temporary_folder,
            clip_filename
        )
        clipping = (
            'gdal_translate -projwin ' +
            '%(CLIP)s %(PROJECT)s %(OUTPUT)s'
        )
        request_process = clipping % {
            'CLIP': bbox_string.replace(',', ' '),
            'PROJECT': raster_filepath,
            'OUTPUT': output,
        }
    elif geojson:
        output = os.path.join(
            temporary_folder,
            clip_filename
        )
        mask_file = os.path.join(
            temporary_folder,
            filename + '.' + current_date + '.geojson'
        )
        _file = open(mask_file, 'w+')
        _file.write(geojson)
        _file.close()

        masking = ("gdalwarp -dstnodata 0 -q -cutline '%(MASK)s' " +
                   "-crop_to_cutline " +
                   "-dstalpha -of " +
                   "GTiff '%(PROJECT)s' '%(OUTPUT)s'")
        request_process = masking % {
            'MASK': mask_file,
            'PROJECT': raster_filepath,
            'OUTPUT': output,
        }
    else:
        raise Http404('No bbox or geojson in parameters.')

    # generate if output is not created
    if not os.path.exists(output):
        if raster_filepath:
            subprocess.call(request_process, shell=True)

    if os.path.exists(output):
        # Check size
        clipped_size = os.path.getsize(output)

        if not check_file_size(clipped_size):
            response = JsonResponse({
                'error': 'Clipped file size is '
                         'bigger than %s mb' % (
                             int(MAX_CLIP_SIZE) / 1000000
                         )
            })
            response.status_code = 403
            return response

        response = JsonResponse({
            'success': 'Successfully clipping layer',
            'clip_filename': clip_filename
        })
        response.status_code = 200
        return response
    else:
        raise Http404('Project can not be clipped or masked.')


def download_clip(request, layername, clip_filename):
    """Download clipped file.
    Clipping layer by bbox or by geojson.
    :param layername: The layer name in Geonode.
    :type layername: basestring
    :param clip_filename: clipped filename
    :type clip_filename: basestring
    :return: The HTTPResponse with a file.
    """
    # PREPARATION
    layer = Layer.objects.get(
            workspace=layername.split(':')[0],
            name=layername.split(':')[1]
    )

    query = request.GET or request.POST
    params = {
        param.upper(): value for param, value in query.iteritems()}
    current_date = datetime.datetime.today().strftime('%Y-%m-%d_%H-%M-%S')

    # create temp folder
    temporary_folder = os.path.join(
        tempfile.gettempdir(), 'clipped')
    try:
        os.mkdir(temporary_folder)
    except OSError as e:
        pass

    # get file for raster
    raster_filepath = None
    extention = ''

    file_names = []
    try:
        for layerfile in layer.upload_session.layerfile_set.all():
            file_names.append(layerfile.file.path)

        for target_file in file_names:
            if '.tif' in target_file:
                raster_filepath = target_file
                target_filename, extention = os.path.splitext(target_file)
                break
    except AttributeError:
        raster_filepath = layername
        pass

    # get temp filename for output
    filename = os.path.basename(clip_filename)

    output = os.path.join(
        temporary_folder,
        clip_filename
    )

    if os.path.exists(output):
        # Create zip file
        s = StringIO.StringIO()
        zf = zipfile.ZipFile(s, "w")

        zip_subdir = layer.name + '_clipped'
        zip_filename = "%s.zip" % zip_subdir

        files_to_zipped = []
        for filename in file_names:
            if not filename.endswith('.qgs') and \
                    not filename.endswith(extention):
                files_to_zipped.append(filename)

        for fpath in files_to_zipped:
            # Calculate path for file in zip
            fdir, fname = os.path.split(fpath)
            fnames = fname.split('.')
            fname = fnames[0] + '.' + current_date + '.' + fnames[1]
            zip_path = os.path.join(zip_subdir, fname)
            zf.write(fpath, zip_path)

        # Add clipped raster
        opath, oname = os.path.split(output)
        zip_path = os.path.join(zip_subdir, oname)
        zf.write(output, zip_path)

        # Must close zip for all contents to be written
        zf.close()
        resp = HttpResponse(
            s.getvalue(), content_type="application/x-zip-compressed")
        resp['Content-Disposition'] = 'attachment; filename=%s' % zip_filename
        return resp
    else:
        raise Http404('Project can not be clipped or masked.')


class ClipView(View):
    template_name = 'clip_and_ship/clip_page.html'

    def get(self, request, geotiffname):
        context = {
            'geotiffname': geotiffname,
            'resource': {
                'get_tiles_url': "%sgwc/service/gmaps?layers=geonode:%s&zoom={z}&x={x}&y={y}&format=image/png8" % (
                    settings.GEOSERVER_PUBLIC_LOCATION,
                    geotiffname
                ),
                'service_typename': 'geonode:' + geotiffname
            }
        }
        return render(request, self.template_name, context)
