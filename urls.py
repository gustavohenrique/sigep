from django.conf.urls.defaults import *
from django.conf import settings
#from django.contrib import databrowse
from django.contrib import admin
admin.autodiscover()
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    # Example:
    # (r'^sigep/', include('sigep.foo.urls')),
    #(r'^databrowse/(.*)', databrowse.site.root),
    #(r'^$', login_required('django.views.generic.simple.direct_to_template', {'template':'login.html'})),
    (r'^$', 'sigep.client.views.list'),
    (r'^auth/login/','django.contrib.auth.views.login'),
    (r'^auth/logout/','django.contrib.auth.views.logout_then_login'),
    (r'^admin/(.*)', admin.site.root),    
    (r'^client/', include('sigep.client.urls')),
    
)

urlpatterns += patterns('',
  (r'^media/(.*)','django.views.static.serve',{'document_root':settings.MEDIA_ROOT}),  
)
