from django.core.mail import send_mail
from registration.models import RegistrationProfile

def send_activation_email(sender, instance, signal, *args, **kwargs):
    try:
        reg_prof = RegistrationProfile.objects.get(user=instance)
    except RegistrationProfile.DoesNotExist:
        return
    
    if (instance.is_active and
        reg_prof.activation_key == 'EMAIL_VERIFIED'):
        
        send_mail("Your We Have We Need account has been activated",
                  "The account '%s' at We Have We Need has been "
                  "activated by an administrator. Please visit "
                  "http://wehaveweneed.org/login/ to login and "
                  " use the site." % user.username,
                  'webmaster@wehaveweneed.com',
                  [instance.email])
        reg_prof.activation_key = RegistrationProfile.ACTIVATED
        reg_prof.save()
