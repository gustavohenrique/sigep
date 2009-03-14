from django.conf.urls.defaults import patterns, url

urlpatterns = patterns ('sigep.client.views',
  url(r'^list/$', 'list', name='client_list'),
  url(r'^add/$', 'add', name='client_add'),
  url(r'^edit/$', 'edit', name='client_edit'),
  url(r'^update/$', 'update', name='client_update'),
)

urlpatterns += patterns ('sigep.client.ajax',
  url(r'^ajax/datagridx/$', 'datagridx', name='client_ajax_datagridx'),
  url(r'^ajax/deletex/$', 'deletex', name='client_ajax_deletex'),
  url(r'^ajax/comboajax/(?P<modelo>.+)/(?P<foreignkey>.+)/(?P<fieldkey>.+)/$', 'comboajax', name='comboajax'),
)
