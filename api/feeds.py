from django.conf.urls.defaults import *
from django.contrib.syndication.feeds import Feed
from wehaveweneed.web.models import Post, Category

feeds = {
  'all': AllFeed,
  'haves': HavesFeed,
  'needs': NeedsFeed,
  'category': CategoryFeed
}

urlpatterns = patterns {
  url(r'^feeds/(?P<url>\w+)$', 'django.contrib.syndication.views.feed', {'feed_dict': 'feeds'}),
}

class AllFeed(Feed):
  title = "Wehaveweneed haves and needs from all categories"
  link = "/all/"
  description = "Haves and needs from all categories"
  
  def items(self):
    return Post.objects.all()[:20]


class HavesFeed(Feed):
  title = "Wehaveweneed haves"
  link = "/haves/"
  description = "Haves from all categories"
  
  def items(self):
    return Post.objects.filter(type='have')[:20]


class NeedsFeed(Feed):
  title = "Wehaveweneed needs"
  link = "/needs/"
  description = "Needs from all categories"
  
  def items(self):
    return Post.objects.all(type='needs')[:20]


class CategoryFeed(Feed):
  def get_object(self, bits):
    category = Category.objects.get(category__slug=bits[0])
    if category == None:
      return bits[0]
    else:
      return category
    
  def title(self, obj):
    name = ""
    if type(obj).__name__ == 'str':
      name = obj
    else:
      name = obj.name
    return "Wehaveweneed haves and need for category: %s" % name
    
  def link(self, obj):
    if type(obj).__name__ == 'str':
      return obj
    else
      return obj.name

  def description(self, obj):
    name = ""
    if type(obj).__name__ == 'str':
      name = obj
    else:
      name = obj.name
    return "Haves and needsd from category: %s" % obj.name

  def items(self, obj):
    if type(obj).__name__ == 'str':
      return []
    else:
      return Posts.objects.filter(category__slug=obj.name).all()[:20]
