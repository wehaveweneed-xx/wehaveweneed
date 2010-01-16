from django.conf.urls.defaults import *
from piston.resource import Resource
from wehaveweneed.api.handlers import CategoryHandler, PostHandler, PostListHandler

post_list_resource = Resource(PostListHandler)
post_resource = Resource(PostHandler)
category_resource = Resource(CategoryHandler)

urlpatterns = patterns('',

    url(r'^categories.(?P<emitter_format>.+)$', category_resource),

    url(r'^post/(?P<post_id>\d+).(?P<emitter_format>.+)$', post_resource),
    
    url(r'^haves.(?P<emitter_format>.+)$', post_list_resource, {'post_type': 'have'}),
    url(r'^needs.(?P<emitter_format>.+)$', post_list_resource, {'post_type': 'need'}),
    url(r'^(?P<category>[\w-]+)/haves.(?P<emitter_format>.+)$', post_list_resource, {'post_type': 'have'}),
    url(r'^(?P<category>[\w-]+)/needs.(?P<emitter_format>.+)$', post_list_resource, {'post_type': 'need'}),
    url(r'^(?P<category>[\w-]+).(?P<emitter_format>.+)$', post_list_resource),
    
)
