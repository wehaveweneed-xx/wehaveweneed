from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from registration.models import RegistrationProfile
from wehaveweneed.web.models import Post, UserProfile
from wehaveweneed.accounts.utils import verify
from wehaveweneed.accounts.forms import AccountSettingsForm

@login_required
def settings(request):
    updated = False
    try:
        profile = request.user.get_profile()
    except UserProfile.DoesNotExist:
        profile = UserProfile(user=request.user, organization='We Have We Need')
        profile.save()
    posts = Post.objects.filter(contact=request.user)
    if request.method == 'POST':
        form = AccountSettingsForm(request.POST)
        if form.is_valid():
            
            data = form.cleaned_data
            
            request.user.username = data['username']
            request.user.email = data['email']
            request.user.first_name = data['first_name']
            request.user.last_name = data['last_name']
            
            profile.organization = data['organization']
            profile.phone = data['phone']
            profile.twitter = data['twitter']
            
            request.user.save()
            profile.save()
            
            request.user.message_set.create(
                message='Your account settings have been updated.')
            return HttpResponseRedirect(reverse('account_settings'))
            
    else:
        form = AccountSettingsForm({
            'username': request.user.username,
            'email': request.user.email,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'organization': profile.organization,
            'phone': profile.phone,
            'twitter': profile.twitter
        })

    return render_to_response('registration/account_settings.html',
                              RequestContext(request,
                                             {'form': form,
                                              'user': request.user,
                                              'posts': posts}))

def verify_email(request, verification_key,
                 template_name='registration/activate.html',
                 extra_context=None):
    verification_key = verification_key.lower() # Normalize before trying anything with it.
    account = verify(verification_key)

    if extra_context is None:
        extra_context = {}
    context = RequestContext(request)
    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value
    return render_to_response(template_name,
                              { 'account': account},
                              context_instance=context)

@staff_member_required
def admin_activate(request):
    if request.method == 'POST':
        user = User.objects.get(id=request.POST['user_id'])
        user.is_active = True
        user.save()

    profs = RegistrationProfile.objects.filter(
        activation_key='EMAIL_VERIFIED',
        user__is_active=False)


    return render_to_response('registration/admin_activate.html',
                    RequestContext(request,
                                   {'users': [p.user for p in profs]}))


