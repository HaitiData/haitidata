import csv

from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from geonode.layers.models import Layer

from .models import Chart, ChartForm
from wfs_harvest.utils import get_fields


class ChartDetailView(DetailView):
    model = Chart


class ChartCreate(CreateView):
    form_class = ChartForm
    template_name = 'charts_app/chart_form.html'

    def get_initial(self):
        layer_id = self.kwargs['layer_id']
        initial = self.initial.copy()
        initial['layer'] = layer_id
        return initial

    def get_context_data(self, **kwargs):
        layer_id = self.kwargs['layer_id']
        layer = Layer.objects.get(pk=layer_id)
        fieldnames, num_fieldnames = get_fields(layer_id)
        ctx = super(ChartCreate, self).get_context_data(**kwargs)
        ctx['fieldnames'] = fieldnames
        ctx['num_fieldnames'] = num_fieldnames
        ctx['layer'] = layer
        return ctx


class ChartUpdate(UpdateView):
    model = Chart
    fields = '__all__'
    template_name_suffix = '_update_form'


class ChartDelete(DeleteView):
    model = Chart
    success_url = '/'


class ChartList(ListView):
    model = Chart
    fields = '__all__'
    template_name = 'charts_app/chart_list.html'

    def get_context_data(self, **kwargs):
        context = super(ChartList, self).get_context_data(**kwargs)
        return context
