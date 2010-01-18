from django.core.mail import EmailMessage

def send_reply_email(request, post, form):
    subject = "Someone has replied to '%s' on WeHaveWeNeed" % (
        post.title)

    sender = form.cleaned_data.get('email')
    if not sender:
        sender = request.user.email
        
    body = "%s said:\n\n%s" % (sender,
                                    form.cleaned_data['content'])

    to = (post.contact.email,)
    headers = {'Reply-To': sender}

    email = EmailMessage(subject=subject,
                         body=body,
                         from_email='webmaster@wehaveweneed.org',
                         to=to,
                         headers=headers)
    email.send()

