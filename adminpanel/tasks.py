# adminpanel/tasks.py
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def userstatus(email, user_status):
    subject = "Your account status has been changed"
    message = f"This email is to inform you that your account status is now {user_status}."
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])
