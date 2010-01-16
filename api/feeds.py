from django.contrib.syndication.feeds import Feed
from wehaveweneed.web.models import Post, Category

class AllFeed(Feed):
  title = "Wehaveweneed haves and needs from all categories"
  link = "/all/"
  description = "Haves and needs from all categories"
  
  def items(self):
    return Post.objects.all()[:20]


class HaveFeed(Feed):
  title = "Wehaveweneed haves"
  link = "/have/"
  description = "Haves from all categories"
  
  def items(self):
    return Post.objects.filter(type='have')[:20]


class NeedFeed(Feed):
  title = "Wehaveweneed needs"
  link = "/need/"
  description = "Needs from all categories"
  
  def items(self):
    return Post.objects.filter(type='need')[:20]


# Display feed for a specific category
# Unrecognized categories cause an empty list to be generated
# The code for handling unrecognized categories is ugly and needs to be cleaned up
class CategoryFeed(Feed):
  def get_object(self, bits):
    # Currently using only the first bit
    if not len(bits):
      return "category"
    category = Category.objects.get(category__slug=bits[0])
    if not category:
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
    else:
      return obj.name

  def description(self, obj):
    name = ""
    if type(obj).__name__ == 'str':
      name = obj
    else:
      name = obj.name
    return "Haves and needsd from category: %s" % name

  def items(self, obj):
    if type(obj).__name__ == 'str':
      return []
    else:
      return Posts.objects.filter(category__slug=obj.name).all()[:20]
