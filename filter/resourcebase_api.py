from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from geonode.api.resourcebase_api import CommonModelApi, CommonMetaApi
from geonode.layers.models import Layer
from geonode.base.models import Region


class CommonModelApiExt(CommonModelApi):
    def apply_filters(self, request, applicable_filters):
        types = applicable_filters.pop('type', None)
        extent = applicable_filters.pop('extent', None)
        keywords = applicable_filters.pop('keywords__slug__in', None)
        region = applicable_filters.get('regions__name__in', None)
        region_bbox = None
        if region:
            print('region is ', region)
            try:
                region_obj = Region.objects.get(name=region[0]) 
            except Region.DoesNotExist:
                print 'it does not exists'
            else:
                print('db record', region_obj.name_en)
                try:
                    regionbbox_obj = region_obj.regionbbox
                except ObjectDoesNotExist:
                    print 'regionbbox does not exist'
                else:
                    print(str(regionbbox_obj.bbox_x0))
                    bbox = [regionbbox_obj.bbox_x0, regionbbox_obj.bbox_y0, regionbbox_obj.bbox_x1, regionbbox_obj.bbox_y1]
                    bbox_valid = not any(coo is None for coo in bbox)
                    if bbox_valid:
                        region_bbox = ','.join([str(coo) for coo in bbox])
                        del applicable_filters['regions__name__in']
                        extent = None
                        print region_bbox
                    else:
                        print 'bbox not valid'

        semi_filtered = super(
            CommonModelApi,
            self).apply_filters(
            request,
            applicable_filters)
        filtered = None
        if types:
            for the_type in types:
                if the_type in LAYER_SUBTYPES.keys():
                    if filtered:
                        filtered = filtered | semi_filtered.filter(
                            Layer___storeType=LAYER_SUBTYPES[the_type])
                    else:
                        filtered = semi_filtered.filter(
                            Layer___storeType=LAYER_SUBTYPES[the_type])
                else:
                    if filtered:
                        filtered = filtered | semi_filtered.instance_of(
                            FILTER_TYPES[the_type])
                    else:
                        filtered = semi_filtered.instance_of(
                            FILTER_TYPES[the_type])
        else:
            filtered = semi_filtered

        if extent:
            filtered = self.filter_bbox(filtered, extent)

        if keywords:
            filtered = self.filter_h_keywords(filtered, keywords)

        if region_bbox:
            filtered = self.filter_bbox(filtered, region_bbox)
            print 'filtering by bbox: ', region_bbox

        return filtered


class LayerExtResource(CommonModelApiExt):
    """Layer Ext API"""

    class Meta(CommonMetaApi):
        queryset = Layer.objects.distinct().order_by('-date')
        if settings.RESOURCE_PUBLISHING:
            queryset = queryset.filter(is_published=True)
        resource_name = 'layers'
        excludes = ['csw_anytext', 'metadata_xml']
