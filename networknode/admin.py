# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from sigep.networknode.models import *

class PlanAdmin(ModelAdmin):
  list_display = ('plan','downstream_min','downstream_max','upstream_min','upstream_max','price')
  ordering = ['plan','downstream_min']
  
class AccessPointAdmin(ModelAdmin):
  list_display = ('accesspoint','ip','location')
  ordering = ['accesspoint','ip']

admin.site.register(AccessPoint, AccessPointAdmin)
admin.site.register(Proxy)
admin.site.register(Plan, PlanAdmin)
admin.site.register(Hardware)
