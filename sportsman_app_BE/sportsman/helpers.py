from datetime import datetime, timedelta
from django.core.mail import EmailMessage

from os import environ
import jwt
from django.conf import settings


def send_confirmation_email(email):
    expiration_time = datetime.utcnow() + timedelta(hours=3)
    token = jwt.encode({'email': email, 'exp': expiration_time}, settings.SECRET_KEY)
    confirmation_url = environ.get('CONFIRMATION_EMAIL_PAGE').format(token=token)
    link = '<a href="{confirmation_url}">ovdje</a>'.format(confirmation_url=confirmation_url)

    email_subject = 'Potvrda email adrese'
    email_body = '<p>Hvala sto ste se registrovali. Da biste nastavili koristiti aplikaciju molimo da potvrdite svoju ' \
                 'email adresu {link}</p>'.format(link=link)

    email = EmailMessage(
        email_subject,
        email_body,
        environ.get('DEFAULT_FROM_EMAIL'),
        [email],
        headers={'From': 'Sportsman <{sportsmanMail}'.format(sportsmanMail=environ.get('DEFAULT_FROM_EMAIL'))}
    )

    email.content_subtype = "html"

    email.send()

    return token
