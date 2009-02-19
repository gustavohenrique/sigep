# -*- coding: utf-8 -*-

from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from sigep.client.models import *

class CityAdmin(ModelAdmin):
  list_display = ('city','state')
  list_filter = ('state',)
  ordering = ['city','state']

class NeighborhoodAdmin(ModelAdmin):
  list_display = ('neighborhood','city')
  list_filter = ('city',)
  ordering = ['neighborhood','city']

class StreetAdmin(ModelAdmin):
  list_display = ('street','neighborhood')
  list_filter = ('neighborhood',)
  ordering = ['street','neighborhood']
  

admin.site.register(City, CityAdmin)
admin.site.register(Neighborhood, NeighborhoodAdmin)
admin.site.register(Street, StreetAdmin)
admin.site.register(ClientGroup)
#admin.site.register(Client, ClientAdmin)
admin.site.register(AccessPoint)
admin.site.register(Proxy)
admin.site.register(Plan)
admin.site.register(Hardware)

