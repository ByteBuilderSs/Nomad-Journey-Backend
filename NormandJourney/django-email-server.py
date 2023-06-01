# django-email-server.py
from django.core.mail import send_mail
from django.conf import settings
import requests

api_key = 'YOUR_API_KEY'
api_url = 'https://emailvalidation.abstractapi.com/v1/?api_key=' + api_key


def validate_email(email):
    response = requests.get(api_url + "&email=email")
    is_valid = is_valid(response.content)
    return is_valid


def send(subject, message, recipient):
	is_a_valid_email = validate_email(recipient)
	if is_a_valid_email:
		send_mail(
                subject=subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[recipient])
	else:
		print("Not a valid recipient email, cannot send")