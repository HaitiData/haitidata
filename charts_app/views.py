from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


from geonode.layers.models import Layer

from .models import Chart, ChartForm
from wfs_harvest.utils import get_fields


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)


class ChartDetail(DetailView):
    model = Chart

    def get_object(self, queryset=None):
        obj = super(ChartDetail, self).get_object(queryset=queryset)
        lyr_obj = Layer.objects.get(pk=obj.layer)
        if not self.request.user.has_perm('download_resourcebase', lyr_obj.get_self_resource()):
            raise PermissionDenied
        return obj

    def get_context_data(self, **kwargs):
        context = super(ChartDetail, self).get_context_data(**kwargs)
        return context


class ChartCreate(LoginRequiredMixin, CreateView):
    form_class = ChartForm
    template_name = 'charts_app/chart_update_form.html'

    def get_initial(self):
        layer_id = self.kwargs['layer_id']
        initial = self.initial.copy()
        initial['layer'] = layer_id
        return initial

    def get_context_data(self, **kwargs):
        layer_id = self.kwargs['layer_id']
        layer = Layer.objects.get(pk=layer_id)
        if not self.request.user.has_perm('download_resourcebase', layer.get_self_resource()):
            raise PermissionDenied
        fieldnames, num_fieldnames = get_fields(layer_id)
        ctx = super(ChartCreate, self).get_context_data(**kwargs)
        ctx['fieldnames'] = fieldnames
        ctx['num_fieldnames'] = num_fieldnames
        ctx['layer'] = layer
        return ctx

    def form_valid(self, form):
        if not self.request.user.has_perm('download_resourcebase', form.instance.layer.get_self_resource()):
            raise PermissionDenied
        form.instance.created_by = self.request.user
        return super(ChartCreate, self).form_valid(form)


class ChartUpdate(LoginRequiredMixin, UpdateView):
    model = Chart
    fields = '__all__'
    template_name = 'charts_app/chart_update_form.html'

    def get_object(self, queryset=None):
        obj = super(ChartUpdate, self).get_object(queryset=queryset)
        is_chart_owner = (self.request.user == obj.created_by)
        lyr_obj = Layer.objects.get(pk=obj.layer)
        is_lyr_owner = (self.request.user == lyr_obj.owner)
        if not (self.request.user.is_superuser or is_chart_owner or is_lyr_owner):
            raise PermissionDenied
        return obj

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super(ChartUpdate, self).form_valid(form)


class ChartDelete(LoginRequiredMixin, DeleteView):
    model = Chart
    success_url = '/layers/'

    def get_object(self, queryset=None):
        obj = super(ChartDelete, self).get_object(queryset=queryset)
        is_chart_owner = (self.request.user == obj.created_by)
        lyr_obj = Layer.objects.get(pk=obj.layer)
        is_lyr_owner = (self.request.user == lyr_obj.owner)
        if not (self.request.user.is_superuser or is_chart_owner or is_lyr_owner):
            raise PermissionDenied
        return obj


class ChartList(ListView):
    model = Chart
    fields = '__all__'
    template_name = 'charts_app/chart_list.html'

    def get_context_data(self, **kwargs):
        context = super(ChartList, self).get_context_data(**kwargs)
        return context
