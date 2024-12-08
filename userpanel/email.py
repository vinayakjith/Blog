from django.template import Context
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
def send_review_email(name, email, review):
    context = {
        'name': name,
        'email': email,
        'review': review,
    }
    email_subject = 'Thank you for your review'
    email_body = render_to_string('taskapp/message.html', context)
    my_email = EmailMessage(
        email_subject, email_body,
        settings.DEFAULT_FROM_EMAIL, [email],
    )
    my_email.content_subtype = 'html'
    return my_email.send(fail_silently=False)   