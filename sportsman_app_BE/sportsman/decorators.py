from os import environ

from django.http import HttpResponseNotAllowed, JsonResponse
import jwt
from functools import wraps


def authenticate(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        token = request.COOKIES.get('Authentication')

        if not token:
            return JsonResponse({'message': 'Pristup odbijen. Logirajte se da bi nastavili !'}, status=401)

        try:
            decoded_token = jwt.decode(token, environ.get(
                'SECRET_KEY'), algorithms=['HS256'])
            user_id = decoded_token.get('user_id')

            return func(request, user_id, *args, **kwargs)
        except jwt.ExpiredSignatureError:
            return JsonResponse({'message': 'Pristup odbijen. Logirajte se da bi nastavili !'}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({'message': 'Pristup odbijen. Logirajte se da bi nastavili !'}, status=401)

    return wrapper
