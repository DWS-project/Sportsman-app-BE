from os import environ
from django.core.mail import send_mail
from sportsman.utils import email_verification_token


def send_confirmation_email(user):
    user.confirmation_token = email_verification_token.make_token(user)
    user.save()

    confirmation_url = "http://localhost:8000/authentication/confirm-email?token=" + email_verification_token.make_token(
        user)

    link = '<a href="{{ confirmation_url }}">Klikni me</a>'

    email_subject = 'Potvrda email adrese'
    email_body = 'Hvala sto ste se registrovali. Da biste nastavili koristiti aplikaciju molimo da potvrdite svoju ' \
                 'email adresu ovdje ' + link

    send_mail(
        email_subject,
        email_body,
        environ.get('DEFAULT_FROM_EMAIL'),
        [user.email],
        fail_silently=False
    )
