from django.conf.urls.defaults import *
from piston.resource import Resource
from wehaveweneed.api.handlers import PostHandler

post_resource = Resource(PostHandler)

urlpatterns = patterns('',
    url(r'^haves.(?P<emitter_format>.+)$', post_resource, {'post_type': 'have'}),
    url(r'^needs.(?P<emitter_format>.+)$', post_resource, {'post_type': 'need'}),
    url(r'^(?P<category>\w+)/haves.(?P<emitter_format>.+)$', post_resource, {'post_type': 'have'}),
    url(r'^(?P<category>\w+)/needs.(?P<emitter_format>.+)$', post_resource, {'post_type': 'need'}),
    url(r'^(?P<category>\w+).(?P<emitter_format>.+)$', post_resource),
    url(r'^post/(?P<post_id>\w+).(?P<emitter_format>.+)$', post_resource),
)
