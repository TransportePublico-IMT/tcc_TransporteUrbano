from django.contrib import admin

from .models import Chart, Dashboard

admin.site.register(Dashboard)
admin.site.register(Chart)
