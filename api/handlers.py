from piston.handler import BaseHandler
from wehaveweneed.web.models import Category, Post

class CategoryHandler(BaseHandler):
    allowed_methods = ('GET',)
    fields = ('name','slug')
    model = Category

class PostHandler(BaseHandler):
    allowed_methods = ('GET','POST')
    fields = ('id','type','title','location','priority',
              ('contact', ('first_name','last_name')),
              ('category', ('name','slug')),
              'time_start','time_end','created_at','content')
    model = Post
    
    def read(self, request, post_id):
        return Post.objects.filter(pk=post_id)

class PostListHandler(BaseHandler):
    allowed_methods = ('GET',)
    fields = ('id','type','title','location','priority',
              ('contact', ('first_name','last_name')),
              ('category', ('name','slug')),
              'time_start','time_end','created_at','content')
    model = Post
    
    def read(self, request, post_type=None, category=None):
        posts = Post.objects.all()
        if post_type:
            posts = posts.filter(type=post_type)
        if category:
            posts = posts.filter(category__slug=category)
        return posts
       