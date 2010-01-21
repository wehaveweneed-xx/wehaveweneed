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
from django.db.models import Sum
from registration.models import RegistrationProfile
from wehaveweneed.web.models import *
from wehaveweneed.web.forms import *
from wehaveweneed.web.emails import send_reply_email

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
                message='Your post was created.')
        return HttpResponseRedirect(next)

    if request.is_ajax():
        raise Http404

    return render_to_response(
        'post.html',
        {'form': form },
        context_instance = RequestContext(request)
    )

def viewhaves(request, category=None):
    posts = Post.objects.open().filter(type="have")
    if category:
        posts = posts.filter(category__slug=category)
    return object_list(
        request,
        queryset=posts,
        paginate_by=getattr(settings, 'PAGINATE_POSTS_BY', 10),
        template_name='haves.html',
        template_object_name='post',
        extra_context={ 'category': category },
    )

def viewneeds(request, category=None):
    posts = Post.objects.open().filter(type="need")
    if category:
        posts = posts.filter(category__slug=category)
    return object_list(
        request,
        queryset=posts,
        paginate_by=getattr(settings, 'PAGINATE_POSTS_BY', 10),
        template_name='needs.html',
        template_object_name='post',
        extra_context={ 'category': category },
    )

def home(request):
    posts = Post.objects.open()
    categories = Category.objects.all()

    return object_list(
        request,
        queryset=posts,
        paginate_by=10,
        template_name='index.html',
        template_object_name='post',
        extra_context = { 'categories': categories },
        )

def view_post(request, id):
    post = get_object_or_404(Post, pk=id)
    sent =  False

    if request.method == 'POST':
        if request.user == post.contact:
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                form.save()
                request.user.message_set.create(
                    message='Your post was updated.')
        elif request.user.is_authenticated():
            form = ReplyForm(request.POST)
            if form.is_valid():
                Reply.objects.create(post=post,
                                     sender=request.user,
                                     content=form.cleaned_data['content'])
                send_reply_email(request, post, form)
                request.user.message_set.create(
                    message='Your reply was sent.')
        else:
            raise Http404()

        if 'next' in request.POST:
            next = request.POST['next']
        else:
            next = reverse('home')
        return HttpResponseRedirect(next)


    if request.user == post.contact:
        p = post.__dict__.copy()
        p['category'] = post.category.pk
        form = PostForm(p)
    elif request.user.is_authenticated():
        form = ReplyForm()
    else:
        form = None

    return render_to_response('view_post.html',
                              RequestContext(request,
                                             {'post': post,
                                              'form': form,
                                              'sent': sent}))


def top_needs(request):
    need_water = Post.objects.open().filter(object__iexact='water',
                                        unit__iexact='gallons',
                                        type='need').aggregate(
        total=Sum('number'))['total'] or 0

    have_water = Post.objects.open().filter(object__iexact='water',
                                      unit__iexact='gallons',
                                      type='have').aggregate(
        total=Sum('number'))['total'] or 0

    net_water = need_water - have_water

    return render_to_response('top_needs.html',
                              RequestContext(request,
                                             {'need_water':
                                                  need_water,
                                              'have_water':
                                                  have_water,
                                              'net_water':
                                                  net_water}))
