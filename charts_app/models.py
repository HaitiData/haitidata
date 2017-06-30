from django.db import models
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from geonode.layers.models import Layer

from wfs_harvest.utils import get_featno


def validate_wfs(value):
    lyr = Layer.objects.get(pk=value)
    if lyr.service_type != 'WFS':
        raise ValidationError(_('%(lyr_title)s is not a WFS layer'),
                              code='not_a_wfs',
                              params={'lyr_title': lyr.title})

    feat_no = get_featno(value)
    if feat_no > settings.MAX_CSV_RECORDS:
        raise ValidationError(_('%(lyr_title)s has too many features; '
                                'chart functionality is not available '
                                'for very large datasets'),
                              code='too_many_records',
                              params={'lyr_title': lyr.title})


class Chart(models.Model):
    CHART_TYPES = (
        (0, 'Bar chart'),
        (1, 'Pie chart'),
        (2, 'Donut chart'),
        (3, 'Line chart')
    )

    AGGREGATION_TYPES = (
        (0, 'Sum'),
        (1, 'Mean'),
        (2, 'Category count'),
        (3, 'Max'),
        (4, 'Min'),
    )

    layer = models.ForeignKey(Layer, validators=[validate_wfs])
    title = models.CharField(max_length=128, blank=True)
    category = models.CharField(max_length=200)
    quantity = models.CharField(max_length=200)
    type = models.SmallIntegerField(choices=CHART_TYPES, default=0)
    aggr_type = models.SmallIntegerField(choices=AGGREGATION_TYPES, default=3)
    abstract = models.TextField(blank=True)

    def get_absolute_url(self):
        return reverse('chart_detail', kwargs={'pk': self.pk})
