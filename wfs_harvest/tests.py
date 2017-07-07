import urllib

from django.test import SimpleTestCase
from django.core.urlresolvers import reverse

from . import views

# Create your tests here.
class GetFieldsView(SimpleTestCase):
    def test_non_existing_lyr(self):
        # url = reverse(views.get_fields)
        enc_lyrname = urllib.urlencode({'lyrname': 'idontexist'})
        # complete_url = url + '?' + enc_lyrname
        # self.client.get('/table')
        # self.client.get(complete_url)
        self.assertTrue(False)

    def test_non_existing_field(self):
        # self.client.get(reverse('wfs_harvest:get_fields'))
        self.assertTrue(False)