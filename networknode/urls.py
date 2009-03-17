from django.conf.urls.defaults import patterns, url

urlpatterns = patterns ('sigep.networknode.views',
  url(r'^list/$', 'list', name='networknode_list'),
  url(r'^add/$', 'add', name='networknode_add'),
  url(r'^edit/$', 'edit', name='networknode_edit'),
  url(r'^update/$', 'update', name='networknode_update'),
)

urlpatterns += patterns ('sigep.networknode.ajax',
  url(r'^ajax/datagridx/$', 'datagridx', name='networknode_ajax_datagridx'),
  url(r'^ajax/deletex/$', 'deletex', name='networknode_ajax_deletex'),
  url(r'^ajax/unblock/$', 'unblock', name='networknode_ajax_unblock'),
  url(r'^ajax/unbound/$', 'unbound', name='networknode_ajax_unbound'),
  url(r'^ajax/useproxy/$', 'useproxy', name='networknode_ajax_useproxy'),
)

