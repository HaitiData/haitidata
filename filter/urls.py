from tastypie.api import Api

#from geonode.api.resourcebase_api import LayerResource
from filter.resourcebase_api import LayerExtResource


api_ext = Api(api_name='api')

api_ext.register(LayerExtResource())
