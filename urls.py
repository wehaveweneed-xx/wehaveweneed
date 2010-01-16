from django.conf.urls.defaults import *
from django.contrib import admin
from django.contrib.auth.views import login, logout, password_change
from wehaveweneed.web.views import *

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(wehaveweneed.api.urls)),
    url(r'^login/', 'django.contrib.auth.views.login'),
)
