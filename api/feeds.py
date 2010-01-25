from django.contrib.syndication.feeds import Feed
from wehaveweneed.web.models import Post, Category, UserProfile

class PostFeed(Feed):
    title_template = 'feeds/post_title.html'
    description_template = 'feeds/post_description.html'
    
    def item_author_name(self, post):
        if post.contact:
            author = post.contact.get_full_name() or 'Unknown'
            try:
                author = u"%s, %s" % (author, post.contact.get_profile().organization)
            except UserProfile.DoesNotExist:
                pass
            return author
        return 'Anonymous'
    
    def item_link(self, post):
        return post.get_absolute_url()
        
    def item_pubdate(self, post):
        return post.created_at


class AllFeed(PostFeed):
    title = "Haves and needs from WeHaveWeNeed.org"
    link = "/all/"
    description = "Haves and needs from all categories"

    def items(self):
        return Post.objects.open()[:20]

class HaveFeed(PostFeed):
    title = "Haves from WeHaveWeNeed.org"
    link = "/have/"
    description = "Haves from all categories"

    def items(self):
        return Post.objects.open().filter(type='have')[:20]

class NeedFeed(PostFeed):
    title = "Needs from WeHaveWeNeed.org"
    link = "/need/"
    description = "Needs from all categories"

    def items(self):
        return Post.objects.open().filter(type='need')[:20]


# Display feed for a specific category
# Attempts to avoid 404-errors by returning an empty lists for undefined categories
# If no category was specified (url = /feeds/category) all items are returned
class CategoryFeed(PostFeed):
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
