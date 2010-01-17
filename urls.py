from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.views import login, logout, logout_then_login, password_change
from haystack.views import SearchView
from wehaveweneed.web.views import *

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include('wehaveweneed.api.urls')),
    url(r'^feeds/', include('wehaveweneed.api.feedurls')),
    url(r'^login/', login, { 'template_name': 'registration/login.html' }),
    url(r'^logout/', logout_then_login ),
    url(r'^$', 'django.views.generic.simple.direct_to_template', {'template': 'index.html'}),
    url(r'^account/', 'django.views.generic.simple.direct_to_template', {'template': 'not_yet_implemented.html'}),
    url(r'^register/', 'django.views.generic.simple.direct_to_template', {'template': 'not_yet_implemented.html'}),
    url(r'^haves/', 'web.views.viewhaves', name='web_viewhaves'),
    url(r'^needs/', 'web.views.viewneeds', name='web_viewneeds'),
    url(r'^search/', include('haystack.urls')),
    url(r'^post/', 'web.views.post_create', name='web_postcreate'),
)

if (settings.DEBUG):  
    urlpatterns += patterns('',  
        url(r'^%s/(?P<path>.*)$' % settings.MEDIA_URL.strip('/'), 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),  
    )  
