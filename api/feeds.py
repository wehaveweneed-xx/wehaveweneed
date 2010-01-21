from django.contrib.syndication.feeds import Feed
from wehaveweneed.web.models import Post, Category

class AllFeed(Feed):
  title = "We Have We Need: Haves and needs from all categories"
  link = "/all/"
  description = "Haves and needs from all categories"
  
  def items(self):
    return Post.objects.open()[:20]

  def item_pubdate(self, item):
    return item.created_at


class HaveFeed(Feed):
  title = "We Have We Need: Haves"
  link = "/have/"
  description = "Haves from all categories"
  
  def items(self):
    return Post.objects.open().filter(type='have')[:20]

  def item_pubdate(self, item):
    return item.created_at

class NeedFeed(Feed):
  title = "We Have We Need: Needs"
  link = "/need/"
  description = "Needs from all categories"
  
  def items(self):
    return Post.objects.open().filter(type='need')[:20]

  def item_pubdate(self, item):
    return item.created_at

# Display feed for a specific category
# Attempts to avoid 404-errors by returning an empty lists for undefined categories
# If no category was specified (url = /feeds/category) all items are returned
class CategoryFeed(Feed):
  def get_object(self, bits):
    # Expecting the first bit to be the category slug
    if not len(bits):
      # Always return something
      return [""]
    else:
      return bits
  
  def title(self, obj):
    return "We Have We Need: Haves and needs from category %s" % obj[0]
    
  def link(self, obj):
    return "/category/%s" % obj[0]

  def description(self, obj):
    return "Haves and needs from category %s" % obj[0]

  def items(self, obj):
    # If no category type was specified return all posts
    if not obj[0]:
      return Post.objects.open()[:20]

    try:
      return Post.objects.open().filter(category__slug=obj[0])[:20]
    except:
      return []

  def item_pubdate(self, item):
    return item.created_at
