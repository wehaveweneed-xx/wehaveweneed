# Create your views here.
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.core import serializers
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.views.decorators.http import require_POST
from django.views.generic.list_detail import object_list
from registration.models import RegistrationProfile
from wehaveweneed.web.models import *
from wehaveweneed.web.forms import *

@login_required
def post_create(request):
    
    """
    Renders a form for creating a new ``POST`` instance, validates against that
    form, and creates the new instances.
    """
    form = PostForm(request.POST or None)

    if form.is_valid():
        post = form.save(commit=False)
        post.contact = request.user
        post.save()
        if 'next' in request.POST:
            next = request.POST['next']
        else:
            next = reverse('home')
            
        request.user.message_set.create(
                message=_('Your post was created.'))
        return HttpResponseRedirect(next)
    
    if request.is_ajax():
        raise Http404

    return render_to_response(
        'post.html',
        {'form': form },
        context_instance = RequestContext(request)
    )
post_create = login_required(post_create)
    
def viewhaves(request, category=None):
    posts = Post.objects.filter(type="have")
    if category:
        posts = posts.filter(category__slug=category)
    return object_list(
        request,
        queryset=posts,
        paginate_by=getattr(settings, 'PAGINATE_POSTS_BY', 10),
        template_name='haves.html',
        template_object_name='post'
    )

def viewneeds(request, category=None):
    posts = Post.objects.filter(type="need")
    if category:
        posts = posts.filter(category__slug=category)
    return object_list(
        request,
        queryset=posts,
        paginate_by=getattr(settings, 'PAGINATE_POSTS_BY', 10),
        template_name='needs.html',
        template_object_name='post'
    )

def home(request):
    posts = Post.objects.all()
    categories = Category.objects.all()

    return object_list(
        request,
        queryset=posts,
        paginate_by=10,
        template_name='index.html',
        template_object_name='post',
        extra_context = { 'categories': categories },
        )

@login_required
def account_settings(request):
    updated = False
    if request.method == 'POST':
        form = AccountSettingsForm(request.POST)
        if form.is_valid():
            profile = request.user.get_profile()
            profile.organization = form.cleaned_data['organization']
            profile.save()
            updated = True
    else:
        form = AccountSettingsForm(
            {'organization': request.user.get_profile().organization})

    return render_to_response('registration/account_settings.html',
                              {'form': form, 'user': request.user,
                               'updated': updated})
