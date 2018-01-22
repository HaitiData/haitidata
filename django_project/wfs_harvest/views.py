import urllib
import xml.etree.ElementTree as ET

import requests
from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings

from geonode.layers.models import Layer

from utils import get_featno


def get_fields(request):
    lyrname = request.GET['lyrname']
    params = urllib.urlencode({
        'service':'WFS',
        'version':'1.1.0',
        'request':'DescribeFeatureType',
        'typename':lyrname
    })

    wfs_request = urllib.urlopen('http://localhost/geoserver/ows?%s'
                                 % params)
    content = wfs_request.read()

    root = ET.fromstring(content)
    namespace = root.tag.split('}')[0] + '}'
    xpath = ('./{0}complexType/{0}complexContent/'
             '{0}extension/{0}sequence/{0}element').format(namespace)
    numeric_types = ['byte', 'decimal', 'int', 'integer', 'long', 'short',
                     'boolean', 'double', 'float']
    fields = {}
    for element in root.findall(xpath):
        type = element.attrib['type']
        if not type.startswith('gml:'):
            fields[element.attrib['name']] = type[4:]

    fieldnames = fields.keys()
    num_fieldnames = [k for k, v in fields.iteritems() if v in numeric_types]

    context = {
        'lyrname': lyrname,
        'fieldnames': fieldnames,
        'num_fieldnames': num_fieldnames
    }
    return render(request, 'wfs_harvest/field_choice.html', context)


def get_wfs_csv(request):
    qdict = request.GET
    typename = qdict['lyrname']
    category_field = qdict['category']
    quantity_field = qdict['quantity']

    lyr = Layer.objects.get(typename=typename)
    featno = get_featno(lyr.id)
    if featno > settings.MAX_CSV_RECORDS:
        response = HttpResponse('{0} has too many records; csv download'
                                ' is not available for very large '
                                'datasets'.format(lyr.title))
        response.status_code = 413
        response.reason_phrase = 'REQUEST ENTITY TOO LARGE'
        return response

    payload = {
        'service':'WFS',
        'version':'1.1.0',
        'request':'GetFeature',
        'typename':typename,
        'propertyName':category_field + ',' + quantity_field,
        'outputFormat':'csv',
        'maxFeatures': str(settings.MAX_CSV_RECORDS)
    }
    wfs_baseurl = lyr.link_set.get(link_type='OGC:WFS').url
    USER = settings.OGC_SERVER['default']['USER']
    PASSWD = settings.OGC_SERVER['default']['PASSWORD']

    r = requests.get(wfs_baseurl, params=payload, auth=(USER, PASSWD))

    response = HttpResponse(r.text, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="myfile.csv"'
    return response
