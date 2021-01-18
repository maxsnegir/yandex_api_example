from django.conf.global_settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import AccessToken


def get_token_for_user(user):
    token = AccessToken.for_user(user)
    return {
        'token': str(token),
    }


def send_email(user):
    subject = 'Код подтверждения для API'
    message = f'{user.username}, код подтверждения – {user.confirmation_code}'
    send = send_mail(subject, message, EMAIL_HOST_USER, [user.email],
                     fail_silently=False)
    return send
