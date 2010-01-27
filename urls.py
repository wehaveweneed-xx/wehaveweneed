from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.views import login, logout, logout_then_login, password_change
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic.simple import direct_to_template
from haystack.views import SearchView
from wehaveweneed.search.forms import PostSearchForm
from wehaveweneed.search.views import PostSearchView
from wehaveweneed.web.forms import RegistrationForm

admin.autodiscover()

#  account-related urls
urlpatterns = patterns('',
    #url(r'^accounts/activate/(?P<activation_key>\w+)/$',
    #    'registration.views.activate',
    #    {'extra_context': {'auth_form': AuthenticationForm()}},
    #    name='registration_activate'),
    url(r'^accounts/request/$', 'registration.views.register', {'form_class': RegistrationForm}, name="request_account"),
    url(r'^accounts/settings/$', 'wehaveweneed.accounts.views.settings', name="account_settings"),
    url(r'^register/complete/$', direct_to_template,
           {'template': 'registration/registration_complete.html'},
           name='registration_complete'),
    url(r'^accounts/verify_email/(?P<verification_key>\w+)/$', 'wehaveweneed.accounts.views.verify_email'),
    url(r'^accounts/admin_activate/', 'wehaveweneed.accounts.views.admin_activate'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', { 'next_page': '/' }),
    url(r'^accounts/', include('django.contrib.auth.urls')),
)

# have/need views
urlpatterns += patterns('wehaveweneed.web.views',
    url(r'^category/(?P<category_slug>[-\w]+)/$', 'category', name='category'),
    url(r'^haves/$', 'viewhaves', name='web_viewallhaves'),
    url(r'^haves/(?P<category>[-\w]+)/$', 'viewhaves', name='web_viewhaves'),
    url(r'^needs/$', 'viewneeds', name='web_viewallneeds'),
    url(r'^needs/(?P<category>[-\w]+)/$', 'viewneeds', name='web_viewneeds'),
    url(r'^post/(?P<post_id>\d+)/$', 'view_post', name='view_post'),
    url(r'^post/$', 'post_create', name='web_postcreate'),
    url(r'^$', 'home', name="home"),
)

# other views
urlpatterns += patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include('wehaveweneed.api.urls')),
    url(r'^feeds/', include('wehaveweneed.api.feedurls')),
    url(r'^search/', PostSearchView(form_class=PostSearchForm)),
    url(r'^termsofuse/','django.views.generic.simple.direct_to_template', {'template': 'termsofuse.html'}, name="termsofuse"),
    # deprecate /view/<id>/ in favor of /post/<id>/
    # this keeps the GET and POST behavior consistent
    url(r'^view/(?P<post_id>\d+)/$', 'django.views.generic.simple.redirect_to', {'url': '/post/%(post_id)s/'}),
    
)

if (settings.DEBUG):  
    urlpatterns += patterns('',  
        url(r'^%s/(?P<path>.*)$' % settings.MEDIA_URL.strip('/'), 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),  
    )  
