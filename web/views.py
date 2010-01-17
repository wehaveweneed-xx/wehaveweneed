# Create your views here.
from django.utils.translation import ugettext as _
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from wehaveweneed.web.models import *
from wehaveweneed.web.forms import *
from django.core import serializers
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.views.decorators.http import require_POST
from django.core.urlresolvers import reverse
from wehaveweneed import settings

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
            next = reverse('ev_have')
            
        request.user.message_set.create(
                message=_('Your post was created.'))
        return HttpResponseRedirect(next)
    
    if request.is_ajax():
        raise Http404

    return render_to_response(
        'post.html',
        {'form': form},
        context_instance = RequestContext(request)
    )
post_create = login_required(post_create)
    
def viewhaves(request):
    posts = Post.objects.filter(type="have")
    context ={'posts':posts}
    return render_to_response(
        'haves.html',
        context,
        context_instance=RequestContext(request),
    )

def viewneeds(request):
    posts = Post.objects.filter(type="need")
    context ={'posts':posts}
    return render_to_response(
        'needs.html',
        context,
        context_instance=RequestContext(request),
    )
