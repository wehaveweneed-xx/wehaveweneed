import urlparse
from haystack.query import SearchQuerySet, RelatedSearchQuerySet
from piston.handler import BaseHandler, AnonymousBaseHandler
from piston.utils import rc, validate
from django.contrib.sites.models import Site
from wehaveweneed.web.forms import PostForm
from wehaveweneed.web.models import Category, Post, User

class CategoryHandler(BaseHandler):
    """
    Provides listing of all categories.
    """
    allowed_methods = ('GET',)
    fields = ('name','slug')
    model = Category

class ContactHandler(BaseHandler):
    allowed_methods = ('GET',)
    fields = ('first_name', 'last_name', 'organization')
    model = User

    @classmethod
    def organization(cls, model):
        return model.get_profile().organization

class AnonymousPostHandler(AnonymousBaseHandler):
    model = Post

class PostHandler(BaseHandler):
    """
    Handler for individual posts and listing of posts.
    """
    anonymous = AnonymousPostHandler
    allowed_methods = ('GET','POST')
    fields = ('id', 'type', 'title', 'location', 'priority',
              'contact', 'category', 'time_start', 'time_end',
              'created_at', 'content', 'link')
    model = Post

    @classmethod
    def link(cls, model):
        base = "http://" + Site.objects.get_current().domain
        return urlparse.urljoin(base, model.get_absolute_url())

    def read(self, request, post_id=None, post_type=None, category=None):
        if post_id:
            return Post.objects.get(pk=post_id)
        else:
            posts = Post.objects.open()
            search = SearchQuerySet()
            if post_type:
                posts = posts.filter(type=post_type)
                search = search.filter(type=post_type)
            if category:
                cat = Category.objects.get(slug=category)
                posts = posts.filter(category=cat)
                search = search.filter(category_id=cat.pk)
            q = request.GET.get('q', None)
            if q:
                search = search.filter(content=q)
                posts = posts.filter(id__in=[r.pk for r in search])
            return posts

    @validate(PostForm) # validate against post form
    def create(self, request):
        data = request.POST
        post = self.model(
            title=data['title'],
            type=data['type'],
            priority=data['priority'],
            location=data['location'],
            #time_start=data.get('time_start', None),  #### need to parse time
            #time_end=data.get('time_end', None),
            #category=Category.objects.get(slug=data['category']),
            category=Category.objects.get(pk=data['category']),
            #contact=request.user,
            content=data['content'],
        )
        post.save()
        print post.pk
        return rc.CREATED

