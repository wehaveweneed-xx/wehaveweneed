# Create your views here.
import os
from django.utils.translation import ugettext as _
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.views.decorators.http import require_POST
from django.core.urlresolvers import reverse
from wehaveweneed.main.models import *
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from wehaveweneed import settings

@login_required
def post_create(request):
    
    if request.method == 'POST': # If the form has been submitted...
        form = PostForm(request.POST or None)
        
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            
            post=form.save()
            
                
            if 'next' in request.POST:
                    next = request.POST['next']
            else:
                    #next = reverse('view_all_schedules')
                    next = "/haves"
                    return HttpResponseRedirect(next) # Redirect after POST
        else:
            print 'Attempt to post failed.'
            error = 'Attempt to post failed.'
                
            context = {'form': form, 'error': error}
                    
            return render_to_response('post.html',
                                        context,
                                        context_instance = RequestContext(request),)
    else:
        
        form = PostForm() # An unbound form
        data, errors = {}, {}
    
    return render_to_response(
        'post.html',
        {'form': form},
        context_instance = RequestContext(request),
    )
    
def viewhaves(request):
    posts==Post.objects.filter(type="have")
    context ={'posts':posts}
    return render_to_response(
        'have.html',
        context,
        context_instance=RequestContext(request),
    )

def viewneeds(request):
    posts==Post.objects.filter(type="need")
    context ={'posts':posts}
    return render_to_response(
        'need.html',
        context,
        context_instance=RequestContext(request),