from django.contrib import admin

from .models import Chart


class ChartAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']


admin.site.register(Chart, ChartAdmin)
