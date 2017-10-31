import urllib
import xml.etree.ElementTree as ET

from geonode.layers.models import Layer


def get_fields(layer_id):
    layer = Layer.objects.get(pk=layer_id)
    lyrname = layer.typename
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

    return fieldnames, num_fieldnames


def get_featno(layer_id):
    lyr = Layer.objects.get(pk=layer_id)
    wfs_baseurl = lyr.link_set.get(link_type='OGC:WFS').url

    params = urllib.urlencode({
        'service': 'WFS',
        'version': '1.1.0',
        'request': 'GetFeature',
        'typename': lyr.typename,
        'resultType': 'hits'
    })

    wfs_count_request = urllib.urlopen(wfs_baseurl + '?%s' % params)
    content = wfs_count_request.read()

    root = ET.fromstring(content)

    return int(root.attrib['numberOfFeatures'])
