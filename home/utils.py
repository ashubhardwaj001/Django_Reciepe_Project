from .models import Student
import time
from django.core.mail import send_mail
from django.conf import settings

def run_this_function():

    print("Function started")
    time.sleep(1)  
    print("Function finished")


def send_email_to_client():
    subject = "This is a test email"
    message = "This is a test email sent from Django."
    from_email = settings.EMAIL_HOST_USER
    recipient_list = ["ashu48001@gmail.com"]

    send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=recipient_list,)