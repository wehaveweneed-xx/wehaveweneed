from piston.handler import BaseHandler
from piston.utils import rc, validate
from wehaveweneed.web.forms import PostForm
from wehaveweneed.web.models import Category, Post

class CategoryHandler(BaseHandler):
    """
    Provides listing of all categories.
    """
    allowed_methods = ('GET',)
    fields = ('name','slug')
    model = Category

class PostHandler(BaseHandler):
    """
    Handler for individual posts and listing of posts.
    """
    allowed_methods = ('GET','POST')
    fields = ('id','type','title','location','priority',
              ('contact', ('first_name','last_name')),
              ('category', ('name', 'slug')),
              'time_start','time_end','created_at','content')
    model = Post
    
    def read(self, request, post_id=None, post_type=None, category=None):
        if post_id:
            return Post.objects.filter(pk=post_id)
        else:            
            posts = Post.objects.all()
            if post_type:
                posts = posts.filter(type=post_type)
            if category:
                posts = posts.filter(category__slug=category)
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
       