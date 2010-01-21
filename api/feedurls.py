from django.conf.urls.defaults import *
from wehaveweneed.api.feeds import *

feeds = {
  'all': AllFeed,
  'have': HaveFeed,
  'need': NeedFeed,
  'category': CategoryFeed
}

urlpatterns = patterns ('',
  url(r'(?P<url>\w+)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
)
