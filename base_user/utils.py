from django.contrib.auth import get_user_model
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives, EmailMessage
from django.template.loader import get_template
from django.conf import settings

User = get_user_model()

def temporary_password_send(user, password):
    """ Sends an email with temporary login credentials to the user.
    Args:
        user (User): The user object containing the temporary password.
    """
    subject = strip_tags('Temporary Login Credentials Inside')
    body = get_template('temp_password.html').render({'user':user,'password': password})
    msg = EmailMessage(subject, body, settings.FROM_EMAIL, [user.email])
    msg.content_subtype = "html"
    msg.send()

User.objects.filter(email='t7965@mailinator.com').delete()