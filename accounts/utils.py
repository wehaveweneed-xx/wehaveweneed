from registration.models import RegistrationProfile, SHA1_RE

def verify(verification_key):
    if SHA1_RE.search(activation_key):
        try:
            profile = RegistrationProfile.objects.get(activation_key=activation_key)
        except self.model.DoesNotExist:
            return False
        if not profile.activation_key_expired():
            user = profile.user
            user.save()
            profile.activation_key = 'EMAIL_VERIFIED'
            profile.save()
            return user
    return False
