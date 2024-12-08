from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_otp_email(email, otp):
    subject = "Your OTP for Password Reset"
    message = f"Your OTP is {otp}. It is valid for 10 minutes. Please do not share this with anyone."
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])

@shared_task
def register(email):
    subject = "Explore the cities though Blog app"
    message = f"Thankyou for registering Blog app"
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])



