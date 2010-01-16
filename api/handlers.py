from piston.handler import BaseHandler
from wehaveweneed.web.models import Post

class PostHandler(BaseHandler):
    allowed_methods = ('GET','POST')
    model = Post
    
    def read(self, request, post_id=None, post_type=None, category=None):
        if post_id:
            return Post.objects.filter(pk=post_id)
        else:
            posts = Post.objects.all()
            if post_type:
                posts = posts.filter(type=post_type)
            if category:
                posts = posts.filter(category=category)
            return posts
       