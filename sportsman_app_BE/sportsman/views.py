from datetime import timedelta, timezone
from os import environ
import json
from sqlite3 import IntegrityError

import jwt
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F
from django.forms import model_to_dict
from django.http import JsonResponse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from firebase_admin import storage
from rest_framework.decorators import api_view
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import EmailMessage
from django.conf import settings
from .helpers import send_confirmation_email
from .models import *
from django.utils.crypto import get_random_string
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.response import Response
from django.core.mail import send_mail
from django.core import serializers

from dotenv import load_dotenv

load_dotenv()


# Create your views here.

@swagger_auto_schema(
    tags=['Authentication'],
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING, description='The name field'),
            'surname': openapi.Schema(type=openapi.TYPE_STRING, description='The surname field'),
            'username': openapi.Schema(type=openapi.TYPE_STRING, description='The username field'),
            'email': openapi.Schema(type=openapi.TYPE_STRING, description='The email field'),
            'tel_number': openapi.Schema(type=openapi.TYPE_STRING, description='The telephone number field'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description='The password field'),
            'repeatedPassword': openapi.Schema(type=openapi.TYPE_STRING, description='The repeated password field'),
            'city': openapi.Schema(type=openapi.TYPE_STRING, description='The city field'),
            'age': openapi.Schema(type=openapi.TYPE_INTEGER, description='The age field'),
            'sports': openapi.Schema(type=openapi.TYPE_STRING, description='The interests field'),
        },
        required=['name', 'surname', 'username', 'email', 'tel_number', 'password', 'repeatedPassword', 'city', 'age',
                  'sports']

    )
)
@api_view(['POST'])
def registration_player(request):
    data = request.data
    name = data.get('name')
    surname = data.get('surname')
    username = data.get('username')
    email = data.get('email')
    tel_number = data.get('tel_number')
    password = data.get('password')
    repeated_password = data.get('repeatedPassword')
    city = data.get('city')
    age = data.get('age')
    sports = data.get('interests')
    if not sports:
        interests = ""
    else:
        interests = json.dumps({"interests": sports})
    user = User.objects.filter(email=email)
    if password != repeated_password:
        return JsonResponse({'status': False, 'message': "Lozinke se ne podudaraju"},
                            status=status.HTTP_400_BAD_REQUEST)
    elif len(user) > 0:
        return JsonResponse({'status': False, 'message': "Email je već registrovan."},
                            status=status.HTTP_400_BAD_REQUEST)
    else:
        token = send_confirmation_email(email)

        User.objects.create(**{
            'name': name,
            'surname': surname, 'username': username,
            'email': email,
            "tel_number": tel_number,
            'city': city,
            'age': age,
            'interests': interests,
            'password': make_password(password),
            'confirmation_token': token,
            'email_confirmed': False,
            'user_type': UserType.objects.get(pk=1)
        })

    return JsonResponse({'status': True, 'message': "Uspješno ste se registrovali."},
                        status=status.HTTP_201_CREATED)


@swagger_auto_schema(
    tags=['Authentication'],
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING, description='The name field'),
            'surname': openapi.Schema(type=openapi.TYPE_STRING, description='The surname field'),
            'username': openapi.Schema(type=openapi.TYPE_STRING, description='The username field'),
            'email': openapi.Schema(type=openapi.TYPE_STRING, description='The email field'),
            'tel_number': openapi.Schema(type=openapi.TYPE_STRING, description='The telephone number field'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description='The password field'),
            'repeatedPassword': openapi.Schema(type=openapi.TYPE_STRING, description='The repeated password field'),
            'city': openapi.Schema(type=openapi.TYPE_STRING, description='The city field'),
            'capacity': openapi.Schema(type=openapi.TYPE_INTEGER, description='The capacity field'),
            'street': openapi.Schema(type=openapi.TYPE_STRING, description='The street field'),
            'streetNumber': openapi.Schema(type=openapi.TYPE_STRING, description='The street number field')
        },
        required=['name', 'surname', 'username', 'email', 'tel_number', 'password', 'repeatedPassword', 'city',
                  'capacity', 'street', 'streetNumber', 'type']
    )
)
@api_view(['POST'])
def registration_owner(request):
    data = request.data
    name = data.get('name')
    surname = data.get('surname')
    username = data.get('username')
    email = data.get('email')
    tel_number = data.get('tel_number')
    password = data.get('password')
    repeated_password = data.get('repeatedPassword')
    city = data.get('city')
    capacity = data.get('capacity')
    street = data.get('street')
    street_number = data.get('streetNumber')
    location = json.dumps(
        {"city": city, "street": street, "streetNumber": street_number})
    owner = User.objects.filter(email=email)

    if password != repeated_password:
        return JsonResponse({'status': False, 'message': "Lozinke se ne podudaraju"},
                            status=status.HTTP_400_BAD_REQUEST)
    elif len(owner) > 0:
        return JsonResponse({'status': False, 'message': "Email je već registrovan."},
                            status=status.HTTP_400_BAD_REQUEST)
    else:
        token = send_confirmation_email(email)

        Owner.objects.create(**{
            'name': name,
            'surname': surname, 'username': username,
            'email': email,
            "tel_number": tel_number,
            'password': make_password(password),
            'confirmation_token': token,
            'email_confirmed': False,
            'user_type': UserType.objects.get(pk=2),
            'location': location,
            'capacity': capacity
        })

        return JsonResponse({'status': True, 'message': "Uspješno ste se registrovali."},
                            status=status.HTTP_201_CREATED)


@swagger_auto_schema(
    tags=['Authentication'],
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'email': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL),
            'password': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_PASSWORD),
        },
        required=['email', 'password'],
    ),
    responses={
        200: 'Successful login response',
    },
)
@api_view(['POST'])
def login(request):
    data = request.data
    response = Response()
    email = data.get('email', None)
    password = data.get('password', None)

    if User.objects.filter(email=email).exists():
        user = User.objects.get(email=email)
        is_password_valid = check_password(password, user.password)
        if is_password_valid:
            print('hh')
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh)
            user.access_token = access_token

            response.set_cookie(
                "Authentication", access_token, 86400, httponly=True)

            response.data = {"user": {"id": user.id,
                                      "email": user.email, "username": user.username,
                                      "tel_number": user.tel_number, "age": user.age, "city": user.city,
                                      "interests": user.interests,
                                      "name": user.name, "surname": user.surname, "user_type": user.user_type.id,
                                      "picture": user.picture}}
            response.message = "Login successfully"

            return response
        else:
            return JsonResponse({"message": "Invalid username or password!!",
                                 "data": {},
                                 }, status=status.HTTP_400_BAD_REQUEST)
    return JsonResponse({"message": "Invalid username or password!!",
                         "data": {},
                         }, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    tags=['Authentication'],
    method='post',
    responses={
        200: 'Successful logout response',
    },
)
@api_view(['POST'])
def logout(request):
    if request.user.is_authenticated:
        request.user.access_token = None
        request.user.save()

    response = Response({"message": "Logged out successfully.", "data": {}})
    response.delete_cookie("Authentication")
    return response


@swagger_auto_schema(
    tags=['Sport Hall'],
    method='get',
    manual_parameters=[
        openapi.Parameter('price', openapi.IN_QUERY,
                          description='The price field', type=openapi.TYPE_STRING),
        openapi.Parameter('city', openapi.IN_QUERY,
                          description='The city field', type=openapi.TYPE_STRING),
        openapi.Parameter('date', openapi.IN_QUERY,
                          description='The date field', type=openapi.TYPE_STRING),
        openapi.Parameter('time', openapi.IN_QUERY,
                          description='The time field', type=openapi.TYPE_STRING),
        openapi.Parameter('text', openapi.IN_QUERY,
                          description='The searchbar text field', type=openapi.TYPE_STRING),
        openapi.Parameter('sort_type', openapi.IN_QUERY,
                          description='The type sorting field', type=openapi.TYPE_STRING),
        openapi.Parameter('sort_price', openapi.IN_QUERY,
                          description='The price sorting field', type=openapi.TYPE_STRING),
        openapi.Parameter('sports', openapi.IN_QUERY,
                          description='The sports field', type=openapi.TYPE_STRING),
        openapi.Parameter('type', openapi.IN_QUERY,
                          description='The type field', type=openapi.TYPE_INTEGER),
    ]
)
@api_view(['GET'])
def get_filtered_sport_halls(request):
    price = request.GET.get('price')
    city = request.GET.get('city')
    sports = request.GET.getlist('sports[]')
    sport_halls_type = request.GET.getlist('type[]')
    date = request.GET.get('date')
    time = request.GET.get('time')
    search_text = request.GET.get('searchText')
    sort_type = request.GET.get('sort_type')
    sort_price = request.GET.get('sort_price')

    queryset = SportHall.objects.all()

    if city:
        queryset = queryset.filter(city=city)

    if sport_halls_type:
        queryset = queryset.filter(type__in=sport_halls_type)

    if price:
        queryset = queryset.filter(price__lte=price)

    if search_text:
        queryset = queryset.filter(title__icontains=search_text)

    if sort_type:
        if sort_type == 1:
            queryset = queryset.order_by('type')
        elif sort_type == 2:
            queryset = queryset.order_by('-type')

    if sort_price:
        if sort_price == 1:
            queryset = queryset.order_by('price')
        elif sort_price == 2:
            queryset = queryset.order_by('-price')

    filtered_items = []
    for item in queryset:
        sports_string = item.sports
        sports_list = json.loads(sports_string)
        if any(sport in sports_list['sports'] for sport in sports):
            filtered_items.append(model_to_dict(item))

    return JsonResponse({'status': True, 'data': filtered_items}, status=status.HTTP_200_OK)


@swagger_auto_schema(
    tags=['Authentication'],
    method='put',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'email': openapi.Schema(type=openapi.TYPE_STRING),
        },
        required=['email']
    ),
    responses={
        200: openapi.Response('OK'),
        404: openapi.Response('Not Found'),
    }
)
@api_view(['PUT'])
def forgot_password(request):
    email = request.data.get('email')
    if User.objects.filter(email=email).exists() is False:
        return JsonResponse({'status': False, 'message': 'Korisnik sa unesenim emailom nije registrovan'},
                            status=status.HTTP_404_NOT_FOUND)
    else:
        if User.objects.filter(email=email).exists():
            password = get_random_string(8)
            user = User.objects.get(email=email)
            user.password = make_password(password)
            user.save()
            send_mail(
                'PROMJENA LOZINKE',
                'Vaša nova lozinka je ' + password,
                environ.get('DEFAULT_FROM_EMAIL'),
                [email],
                fail_silently=False)
            return JsonResponse({'status': True, 'message': 'Nova lozinka Vam je poslana na ' + email},
                                status=status.HTTP_200_OK)


@swagger_auto_schema(
    tags=['Player'],
    method='get',
    responses={
        200: "OK",
    }
)
@api_view(['GET'])
def get_all_players(request):
    users = list(User.objects.filter(owner__isnull=True).values(
        'id', 'name', 'surname', 'username', 'city', 'age', 'interests', 'picture'))
    return JsonResponse(users, safe=False, status=status.HTTP_200_OK)


@swagger_auto_schema(
    tags=['Owner'],
    method='get',
    responses={
        200: "OK",
    }
)
@api_view(['GET'])
def get_all_owners(request):
    owners = list(User.objects.filter(owner__isnull=False).values(
        'id', 'name', 'surname', 'location', 'username', 'capacity', 'picture', 'tel_number'))
    return JsonResponse(owners, safe=False, status=status.HTTP_200_OK)


@swagger_auto_schema(
    tags=['Sport Hall'],
    method='get',
    manual_parameters=[
        openapi.Parameter('price', openapi.IN_QUERY,
                          description='The price field', type=openapi.TYPE_STRING),
        openapi.Parameter('city', openapi.IN_QUERY,
                          description='The city field', type=openapi.TYPE_STRING),
        openapi.Parameter('date', openapi.IN_QUERY,
                          description='The date field', type=openapi.TYPE_STRING),
        openapi.Parameter('time', openapi.IN_QUERY,
                          description='The time field', type=openapi.TYPE_STRING),
        openapi.Parameter('text', openapi.IN_QUERY,
                          description='The searchbar text field', type=openapi.TYPE_STRING),
        openapi.Parameter('sort_type', openapi.IN_QUERY,
                          description='The type sorting field', type=openapi.TYPE_STRING),
        openapi.Parameter('sort_price', openapi.IN_QUERY,
                          description='The price sorting field', type=openapi.TYPE_STRING),
        openapi.Parameter('sports', openapi.IN_QUERY,
                          description='The sports field', type=openapi.TYPE_STRING),
        openapi.Parameter('type', openapi.IN_QUERY,
                          description='The type field', type=openapi.TYPE_INTEGER),
    ]
)
@api_view(['GET'])
def get_all_sport_halls(request):
    price = request.GET.get('price')
    city = request.GET.get('city')
    sports = request.GET.getlist('sports[]')
    sport_halls_type = request.GET.getlist('type[]')
    date = request.GET.get('date')
    time = request.GET.get('time')
    search_text = request.GET.get('searchText')
    sort_type = request.GET.get('sort_type')
    sort_price = request.GET.get('sort_price')

    queryset = SportHall.objects.all()

    if city:
        queryset = queryset.filter(city=city)

    if sport_halls_type:
        queryset = queryset.filter(type__in=sport_halls_type)

    if price:
        queryset = queryset.filter(price__lte=price)

    if search_text:
        queryset = queryset.filter(title__icontains=search_text)

    if sort_type:
        if sort_type == "1":
            queryset = queryset.order_by('type')
        elif sort_type == "2":
            queryset = queryset.order_by('-type')

    if sort_price:
        if sort_price == "1":
            queryset = queryset.order_by('price')
        elif sort_price == "2":
            queryset = queryset.order_by('-price')

    filtered_items = []
    for item in queryset:
        sports_string = item.sports
        sports_list = json.loads(sports_string)
        if any(sport in sports_list['sports'] for sport in sports):
            filtered_items.append(model_to_dict(item))

    if not any([price, city, sports, sport_halls_type, date, time, search_text, sort_type, sort_price]):
        filtered_items = SportHall.objects.all()

    return Response({'status': True, 'data': filtered_items}, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='get',
    tags=['Player'],
    responses={
        200: "OK",
        404: "User not found"
    }
)
@api_view(['GET'])
def get_player_data(request, id):
    try:
        user = list(User.objects.filter(id=id).values())
        return JsonResponse(user, safe=False, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return JsonResponse({"error": "Korisnik nije pronađen"}, status=status.HTTP_404_NOT_FOUND)


@swagger_auto_schema(
    method='put',
    tags=['Player'],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING, description='The name field'),
            'surname': openapi.Schema(type=openapi.TYPE_STRING, description='The surname field'),
            'username': openapi.Schema(type=openapi.TYPE_STRING, description='The username field'),
            'tel_number': openapi.Schema(type=openapi.TYPE_STRING, description='The telephone number field'),
            'city': openapi.Schema(type=openapi.TYPE_STRING, description='The city field'),
            'age': openapi.Schema(type=openapi.TYPE_INTEGER, description='The age field'),
        },
        required=['name', 'surname', 'username', 'tel_number', 'city', 'age']

    ),
    responses={
        200: "OK",
        404: "User not found"
    }
)
@api_view(['PUT'])
def update_player_data(request, id):
    try:
        user = User.objects.get(id=id)
        data = request.data
        user.username = data.get('username')
        user.name = data.get('name')
        user.surname = data.get('surname')
        user.tel_number = data.get('tel_number')
        user.city = data.get('city')
        user.age = data.get('age')
        user.save()
        return JsonResponse({'status': True, 'message': 'Podatci uspješno promijenjeni'}, status=status.HTTP_200_OK)
    except:
        return JsonResponse({'status': False, 'message': 'Korisnik nije pronađen'}, status=status.HTTP_404_NOT_FOUND)


@swagger_auto_schema(
    tags=['Authentication'],
    method='put',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'new_password': openapi.Schema(type=openapi.TYPE_STRING, description='The new password field'),
            'new_repeated_password': openapi.Schema(type=openapi.TYPE_STRING,
                                                    description='The new repeated password field'),
            'old_password': openapi.Schema(type=openapi.TYPE_STRING, description='The old password field'),
        },
        required=['new_password', 'new_repeated_password', 'old_password']
    ),
    responses={
        200: "OK",
        404: "User not found",
        400: "Bad request",
    }
)
@api_view(['PUT'])
def update_user_password(request, id):
    try:
        user = User.objects.get(id=id)
        print(user)
        data = request.data
        old_password = data.get('oldPassword')
        new_password = data.get('newPassword')
        new_repeated_password = data.get('newRepeatedPassword')
        is_password_valid = check_password(old_password, user.password)
        print(is_password_valid)
        if is_password_valid:
            if new_password == new_repeated_password:
                user.password = make_password(new_password)
                user.save()
                return JsonResponse({'status': True, 'message': 'Lozinka uspješno promijenjena'},
                                    status=status.HTTP_200_OK)
            else:
                return JsonResponse({'status': False, 'message': "Lozinke se ne podudaraju"},
                                    status=status.HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse({'status': False, 'message': "Pogrešna lozinka"}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return JsonResponse({'status': False, 'message': 'Korisnik ne postoji'}, status=status.HTTP_404_NOT_FOUND)


@swagger_auto_schema(
    method='put',
    tags=['Player'],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'photo': openapi.Schema(type=openapi.TYPE_FILE, description='Photo field'),
        },
        required=['photo']
    ),
    responses={
        200: "OK",
        404: "User not found",
    }
)
@api_view(['PUT'])
def update_player_photo(request, id):
    uploaded_file = request.FILES.get('photo')
    user = User.objects.get(id=id)
    if uploaded_file:
        bucket = storage.bucket()
        filename = uploaded_file.name
        blob = bucket.blob(filename)
        blob.content_type = 'image/jpeg'
        blob.upload_from_file(uploaded_file)
        blob.make_public()
        image_url = blob.public_url
        user.picture = image_url
        user.save()
        return JsonResponse({'status': True, 'message': 'Slika profila uspješno promijenjena'},
                            status=status.HTTP_200_OK)
    else:
        return JsonResponse({'status': False, 'message': 'Korisnik nije pronađen'},
                            status=status.HTTP_404_NOT_FOUND)


@swagger_auto_schema(
    method='get',
    tags=['Owner'],
    responses={
        200: "OK",
        404: "User not found"
    }
)
@api_view(['GET'])
def get_owner_data(request, id):
    try:
        owner = list(User.objects.filter(user_type=UserType.objects.get(pk=2), id=id).values())
        return JsonResponse(owner, safe=False, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return JsonResponse({"error": "Korisnik nije pronađen"}, status=status.HTTP_404_NOT_FOUND)


@swagger_auto_schema(
    method='put',
    tags=['Owner'],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING, description='The name field'),
            'surname': openapi.Schema(type=openapi.TYPE_STRING, description='The surname field'),
            'username': openapi.Schema(type=openapi.TYPE_STRING, description='The username field'),
            'tel_number': openapi.Schema(type=openapi.TYPE_STRING, description='The telephone number field'),
            'city': openapi.Schema(type=openapi.TYPE_STRING, description='The city field'),
            'capacity': openapi.Schema(type=openapi.TYPE_INTEGER, description='The capacity field'),
            'street': openapi.Schema(type=openapi.TYPE_STRING, description='The street field'),
            'streetNumber': openapi.Schema(type=openapi.TYPE_STRING, description='The street number field'),
            'type': openapi.Schema(type=openapi.TYPE_STRING, description='The type field'),
        },
        required=['name', 'surname', 'username', 'tel_number', 'city',
                  'capacity', 'street', 'streetNumber', 'type']
    )
)
@api_view(['PUT'])
def update_owner_data(request, id):
    try:
        owner = User.objects.get(id=id)
        data = request.data
        owner.username = data.get('username')
        owner.name = data.get('name')
        owner.surname = data.get('surname')
        owner.tel_number = data.get('tel_number')
        city = data.get('city')
        street = data.get('street')
        street_number = data.get('streetNumber')
        location = json.dumps(
            {"city": city, "street": street, "streetNumber": street_number})
        owner.location = location
        owner.capacity = data.get('capacity')
        owner.type = data.get('type')
        owner.save()
        return JsonResponse({'status': True, 'message': 'Podatci uspješno promijenjeni'}, status=status.HTTP_200_OK)
    except:
        return JsonResponse({'status': False, 'message': 'Korisnik nije pronađen'}, status=status.HTTP_404_NOT_FOUND)


@swagger_auto_schema(
    tags=['Sport Hall'],
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'title': openapi.Schema(type=openapi.TYPE_STRING),
            'city': openapi.Schema(type=openapi.TYPE_STRING),
            'address': openapi.Schema(type=openapi.TYPE_STRING),
            'description': openapi.Schema(type=openapi.TYPE_STRING),
            'status': openapi.Schema(type=openapi.TYPE_STRING),
            'price': openapi.Schema(type=openapi.TYPE_NUMBER),
            'capacity': openapi.Schema(type=openapi.TYPE_INTEGER),
            'owner_id': openapi.Schema(type=openapi.TYPE_INTEGER),
            'pictures': openapi.Schema(type=openapi.TYPE_FILE, format=openapi.FORMAT_BINARY),
        },
        required=['title', 'city', 'address', 'description',
                  'status', 'price', 'capacity', 'owner_id'],
    ),
    responses={
        200: 'Successful response',
        400: 'Bad Request',
    },
)
@api_view(['POST'])
def add_new_sport_hall(request):
    data = request.data
    title = data.get('title')
    city = data.get('city')
    address = data.get('address')
    description = data.get('description')
    sport_hall_status = data.get('status')
    price = data.get('price')
    capacity = data.get('capacity')
    owner_id = data.get('owner_id')
    pictures = data.get('pictures')

    if owner_id is not None:
        sport_hall = SportHall.objects.create(title=title, city=city, address=address,
                                              description=description, status=sport_hall_status, price=price,
                                              capacity=capacity,
                                              pictures=pictures)

        owner = User.objects.get(id=owner_id)
        Owner_SportHall.objects.create(owner=owner, sport_hall=sport_hall)

        return JsonResponse(
            {'data': {title, city, address, description, price}, 'message': 'Uspješno kreiran novi teren.'},
            status=status.HTTP_200_OK)
    else:
        return JsonResponse({'data': {}, 'message': 'Došlo je do greške.'}, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='get',
    tags=['Sport Hall'],
    manual_parameters=[
        openapi.Parameter('owner_id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='ID of the owner'),
        openapi.Parameter('sporthall_id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
                          description='ID of the sport hall'),
    ],
    responses={
        200: openapi.Response(description='Success', schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'data': openapi.Schema(type=openapi.TYPE_OBJECT, description='Data object'),
            },
        )),
        404: openapi.Response(description='Not Found', schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'data': openapi.Schema(type=openapi.TYPE_OBJECT, description='Empty data object'),
            },
        )),
    }
)
@api_view(['GET'])
def get_sport_hall(request):
    data = request.GET.data
    owner_id = data.get('owner_id')
    sport_hall_id = data.get('sporthall_id')
    owner = list(User.objects.get(user_type=UserType.objects.get(pk=2), id=owner_id))
    sport_hall = SportHall.objects.get(id=sport_hall_id)
    array_of_sport_halls = [owner, sport_hall]
    try:
        sport_halls_of_owner = Owner_SportHall.objects.filter(
            owner_id_id=owner_id)
        for sport_hall in sport_halls_of_owner:
            if int(sport_hall.owner_id_id) == int(owner_id):
                array_of_sport_halls.append(sport_hall)
                break
    except:
        obj = serializers.serialize('json', array_of_sport_halls)
        return JsonResponse({'data': json.loads(obj)}, status=status.HTTP_404_NOT_FOUND)
    obj = serializers.serialize('json', array_of_sport_halls)
    return JsonResponse({'data': json.loads(obj)}, status=status.HTTP_200_OK)


@swagger_auto_schema(
    tags=['Sport Hall'],
    method='delete',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'sporthall_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the sport hall'),
        },
        required=['sporthall_id'],
        example={
            'sporthall_id': 1
        }
    ),
    responses={
        200: openapi.Response(description='Success', schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'message': openapi.Schema(type=openapi.TYPE_STRING, description='A message indicating the result'),
                'data': openapi.Schema(type=openapi.TYPE_OBJECT, properties={})
            }
        )),
        404: openapi.Response(description='Not Found'),
    }
)
@api_view(['DELETE'])
def remove_sport_hall(request):
    sporthall_id = request.data.get('sporthall_id')

    try:
        sporthall = SportHall.objects.get(id=sporthall_id)
        sporthall.delete()
        return JsonResponse({'message': "Uspješno uklonjen teren.", 'data': {}}, status=status.HTTP_200_OK)
    except SportHall.DoesNotExist:
        return JsonResponse({'message': "Došlo je do greške.", 'data': {}}, status=status.HTTP_404_NOT_FOUND)


@swagger_auto_schema(
    tags=['Sport Hall'],
    method='patch',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'sporthall_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the sport hall'),
            'status': openapi.Schema(type=openapi.TYPE_STRING, description='New status for the sport hall'),
        },
        required=['sporthall_id', 'status'],
        example={
            'sporthall_id': 1,
            'status': 'open'
        }
    ),
    responses={
        200: openapi.Response(description='Success', schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'message': openapi.Schema(type=openapi.TYPE_STRING, description='A message indicating the result'),
                'data': openapi.Schema(type=openapi.TYPE_OBJECT, properties={})
            }
        )),
        404: "Not Found"
    }
)
@api_view(['PATCH'])
def change_sport_hall_status(request):
    data = request.data
    sport_hall_id = data.get('sporthall_id')
    sport_hall_status = data.get('status')

    try:
        sport_hall = SportHall.objects.get(id=sport_hall_id)
        sport_hall.status = sport_hall_status
        sport_hall.save()
        obj = serializers.serialize('json', [sport_hall])  # Serialize as a list
        return JsonResponse({'data': json.loads(obj)}, status=200)
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'SportHall not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@swagger_auto_schema(
    method='post',
    tags=['Team'],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING),
            'id': openapi.Schema(type=openapi.TYPE_INTEGER),
        },
        required=['name', 'id'],
    ),
    responses={
        201: openapi.Response(description='Success', schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'success': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                'message': openapi.Schema(type=openapi.TYPE_STRING),
            },
        )),
        400: openapi.Response(description='Bad Request', schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'error': openapi.Schema(type=openapi.TYPE_STRING),
                'details': openapi.Schema(type=openapi.TYPE_STRING),
            },
        )),
    }
)
@api_view(['POST'])
def create_team(request):
    name = request.data.get('name')
    lead_id = request.data.get('id')

    try:
        team_lead = Team.objects.create(team_lead_id_id=lead_id)
        PermanentTeams.objects.create(team_name=name, team_id_id=team_lead.id)
        return JsonResponse({'success': True, 'message': 'Uspješno kreiran tim'}, status=201)
    except IntegrityError as e:
        return JsonResponse({'error': 'Kreiranje tima nije uspjelo', 'details': str(e)}, status=400)
    except Exception as e:
        return JsonResponse({'error': 'Greska prilikom kreiranja tima', 'details': str(e)}, status=400)


@swagger_auto_schema(
    method='get',
    tags=['Team'],
    manual_parameters=[
        openapi.Parameter(
            name='id',
            in_=openapi.IN_QUERY,
            description='ID of the team lead',
            type=openapi.TYPE_INTEGER,
            required=True,
        ),
    ],
    responses={
        200: openapi.Response(description='Success', schema=openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'name': openapi.Schema(type=openapi.TYPE_STRING),
                    'members': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                            'name': openapi.Schema(type=openapi.TYPE_STRING),
                        },
                    )),
                },
            ),
        )),
    }
)
@api_view(['GET'])
def get_perm_teams(request):
    lead_id = request.GET.get('id')
    list_of_teams = PermanentTeams.objects.filter(team_id__team_lead_id_id=lead_id)
    res = serializers.serialize('json', list_of_teams)
    data = []

    for team in serializers.deserialize('json', res):
        queryset1 = TeamMembers.objects.filter(team_id_id=team.object.team_id_id)
        res2 = serializers.serialize('json', queryset1)

        if len(res2) != 0:
            members = []

            for member in serializers.deserialize('json', res2):
                queryset2 = User.objects.filter(id=member.object.user_id_id)
                res3 = serializers.serialize('json', queryset2)

                members.append(res3)

            data.append({
                'id': team.object.team_id.id,
                'name': team.object.team_name,
                'members': members
            })

        else:
            data.append({
                'id': team.object.team_id.id,
                'name': team.object.team_name,
                'members': {}
            })

    return JsonResponse(data, safe=False)


@swagger_auto_schema(
    method='delete',
    tags=['Team'],
    manual_parameters=[
        openapi.Parameter(
            name='id',
            in_=openapi.IN_QUERY,
            description='ID of the team to delete',
            type=openapi.TYPE_INTEGER,
            required=True,
        ),
    ],
    responses={
        200: openapi.Response(description='Success', schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'message': openapi.Schema(type=openapi.TYPE_STRING),
                'data': openapi.Schema(type=openapi.TYPE_OBJECT),
            },
        )),
        404: openapi.Response(description='Not Found', schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'error': openapi.Schema(type=openapi.TYPE_STRING),
            },
        )),
        400: openapi.Response(description='Bad Request', schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'error': openapi.Schema(type=openapi.TYPE_STRING),
            },
        )),
    }
)
@api_view(['DELETE'])
def delete_team(request):
    team_id = request.GET.get('id')

    try:
        team = PermanentTeams.objects.get(id=team_id)
        team.delete()
        return JsonResponse({'message': "Uspješno uklonjen tim.", 'data': {}}, status=status.HTTP_200_OK)
    except PermanentTeams.DoesNotExist:
        return JsonResponse({'error': 'Tim nije pronađen.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='post',
    tags=['Team'],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the team leader'),
            'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username of the team member to invite'),
            'team_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the team'),
        },
        required=['id', 'username', 'team_id'],
    ),
    responses={
        200: openapi.Response(description='Success', schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'message': openapi.Schema(type=openapi.TYPE_STRING, description='Success message'),
                'memberName': openapi.Schema(type=openapi.TYPE_STRING, description='Username of the invited member'),
            },
        )),
    }
)
@api_view(['POST'])
def invite_team_member(request):
    lead_id = request.data.get('id')
    name = request.data.get('username')
    team_id = request.data.get('team_id')
    user = User.objects.get(username=name)
    current_time = timezone.localtime(timezone.now())
    formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S')
    formatted_time = (current_time + timedelta(hours=2)).strftime('%Y-%m-%d %H:%M:%S')
    team_name = PermanentTeams.objects.get(id=team_id)
    details_data = {
        'team_id': team_id,
        'team_name': team_name.team_name,
    }
    details_json = json.dumps(details_data)

    Invitations.objects.create(recipient_id=user.id, sender_id=lead_id, time_sent=formatted_time,
                               status=0, details=details_json)
    response_data = {
        'message': 'Invitation sent successfully',
        'memberName': name,

    }

    return JsonResponse(response_data)


@swagger_auto_schema(
    method='delete',
    tags=['Team'],
    manual_parameters=[
        openapi.Parameter('email', openapi.IN_QUERY, type=openapi.TYPE_STRING, description='Email of the team member'),
        openapi.Parameter('teamId', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='ID of the team'),
    ],
    responses={
        200: openapi.Response(description='Success', schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'message': openapi.Schema(type=openapi.TYPE_STRING, description='Success message'),
                'data': openapi.Schema(type=openapi.TYPE_OBJECT, description='Empty data object'),
            },
        )),
        404: openapi.Response(description='Not Found', schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'error': openapi.Schema(type=openapi.TYPE_STRING, description='Error message'),
            },
        )),
    }
)
@api_view(['DELETE'])
def delete_team_member(request):
    email = request.GET.get('email')
    team_id = request.GET.get('teamId')

    try:
        user = User.objects.get(email=email)
        user_id = user.id

        try:
            team_member = TeamMembers.objects.get(user_id_id=user_id, team_id_id=team_id)
            team_member.delete()
            return JsonResponse({'message': "Uspješno uklonjen član tima.", 'data': {}}, status=status.HTTP_200_OK)
        except TeamMembers.DoesNotExist:
            return JsonResponse({'error': 'Ne postoji taj clan u timu.'}, status=status.HTTP_404_NOT_FOUND)
    except User.DoesNotExist:
        return JsonResponse({'error': 'Korisnik ne postoji.'}, status=status.HTTP_404_NOT_FOUND)


@swagger_auto_schema(
    tags=['Authentication'],
    method='post',
    manual_parameters=[
        openapi.Parameter('token', openapi.IN_QUERY, description='Token',
                          type=openapi.TYPE_STRING),
    ],
    responses={
        200: openapi.Response(description='Success', schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'token': openapi.Schema(type=openapi.TYPE_STRING, description='Token'),
            }
        )),
        404: "Not Found",
        500: "Internal Server Error"
    }
)
@api_view(['POST'])
def confirm_email(request):
    try:
        token = request.GET.get('token')
        decoded_token = jwt.decode(token, settings.SECRET_KEY)
        user = User.objects.get(email=decoded_token['email'])
        user.email_confirmed = True
        user.confirmation_token = None

        user.save()
        return JsonResponse(
            {'message': 'Email uspjesno potvrdjen'},
            status=status.HTTP_201_CREATED)

    except jwt.ExpiredSignatureError:
        return JsonResponse({'message': 'Token istekao'}, status=status.HTTP_410_GONE)
    except jwt.InvalidTokenError:
        return JsonResponse({'message': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        return JsonResponse({'message': 'Korisnik ne postoji'}, status=status.HTTP_404_NOT_FOUND)


@swagger_auto_schema(
    tags=['Authentication'],
    method='post',
    manual_parameters=[
        openapi.Parameter('email', openapi.IN_QUERY, description='Email',
                          type=openapi.TYPE_STRING),
    ],
    responses={
        200: openapi.Response(description='Success', schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email'),
            }
        )),
        404: "Not Found",
        201: "Top"
    }
)
@api_view(['POST'])
def resend_confirmation_email(request):
    try:
        email = request.GET.get('email')
        user = User.objects.get(email=email)

        if user.email_confirmed:
            return JsonResponse({'message': 'Email vec potvrdjen'}, status=status.HTTP_400_BAD_REQUEST)

        token = send_confirmation_email(email)
        user.token = token

        user.save()

        return Response({'message': 'Email uspjesno potvrdjen'})
    except User.DoesNotExist:
        return Response({'message': 'Korisnik ne postoji'})


@swagger_auto_schema(
    method='post',
    tags=['Contact'],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING, description='Name'),
            'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email'),
            'message': openapi.Schema(type=openapi.TYPE_STRING, description='Message'),
        },
        required=['name', 'email', 'message'],
        example={
            'name': 'John Doe',
            'email': 'johndoe@example.com',
            'message': 'This is a test message'
        }
    ),
    responses={
        200: openapi.Response(
            description='Success',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'message': openapi.Schema(type=openapi.TYPE_STRING, description='A message indicating the result')
                }
            )
        ),
        400: 'Bad Request',
        500: 'Internal Server Error'
    }
)
@api_view(['POST'])
def contact_us(request):
    name = request.data.get('name')
    email = request.data.get('email')
    message = request.data.get('message')

    user_email_subject = 'Kontakt stranica'
    user_email_body = f'<p>Hvala Vam što ste nas kontaktirali {name}. Administrator će vas kontaktirati u skorije vrijeme na unesenu ' \
                      f'email adresu {email}</p>'

    user_email = EmailMessage(
        user_email_subject,
        user_email_body,
        settings.DEFAULT_FROM_EMAIL,
        [email],
        headers={'From': 'Sportsman <{sportsmanMail}>'.format(
            sportsmanMail=settings.DEFAULT_FROM_EMAIL)}
    )

    user_email.content_subtype = "html"

    user_email.send()

    email_subject = 'Kontakt stranica'
    email_body = f'<p>Osoba {name} Vas je kontaktirala.\n {message}\n ' \
                 f'sa email adresom {email}</p>'

    email = EmailMessage(
        email_subject,
        email_body,
        settings.DEFAULT_FROM_EMAIL,
        [email],
        headers={'From': email, 'To': 'Sportsman <{sportsmanMail}>'.format(
            sportsmanMail=settings.DEFAULT_FROM_EMAIL)}
    )

    email.content_subtype = "html"

    email.send()

    return JsonResponse(
        {'message': 'Poštovani, hvala vam što ste nas kontaktirali! Odgovorit ćemo vam u što skorijem roku.'},
        status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='get',
    tags=['Invitations'],
    responses={
        200: "OK",
        404: "User not found"
    }
)
@api_view(['GET'])
def get_player_invitations(request):
    try:
        data = request.GET
        invitation_id = data.get(id)
        sorting_column = data.get('column')
        sorting_order = data.get('order')
        invite_status = data.get('status')
        invitations = Invitations.objects.filter(recipient_id=invitation_id)

        if sorting_order == 'asc':
            sorted_queryset = list(Invitations.objects.filter(recipient_id=id, status=invite_status)
                                   .values('id', 'sender__username', 'time_sent', 'status', 'details', 'type')
                                   .order_by(sorting_column))

        elif sorting_order == 'desc':
            sorted_queryset = list(Invitations.objects.filter(recipient_id=id, status=invite_status)
                                   .values('id', 'sender__username', 'time_sent', 'status', 'details', 'type')
                                   .order_by('-' + sorting_column))

        else:
            sorted_queryset = list(
                invitations.values('id', 'sender__username', 'time_sent', 'status', 'details', 'type'))

        return JsonResponse(sorted_queryset, safe=False, status=status.HTTP_200_OK)
    except Invitations.DoesNotExist:
        return JsonResponse({"message": "Player invitations not found."}, status=status.HTTP_404_NOT_FOUND)


@swagger_auto_schema(
    method='get',
    tags=['Player'],
    responses={
        200: "OK",
        404: "User not found"
    }
)
@api_view(['GET'])
def get_player_friends(request, id):
    try:
        friends = list(Friends.objects.filter(user1_id=id).values('id', 'user2__username'))
        return JsonResponse(friends, safe=False, status=status.HTTP_200_OK)
    except Friends.DoesNotExist:
        return JsonResponse({"message": "Player's friends not found."}, status=status.HTTP_404_NOT_FOUND)


@swagger_auto_schema(
    tags=['Friends'],
    method='delete',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'friends_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the Friends'),
        },
        required=['friends_id'],
        example={
            'friends_id': 1
        }
    ),
    responses={
        200: openapi.Response(description='Success', schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'message': openapi.Schema(type=openapi.TYPE_STRING, description='A message indicating the result'),
                'data': openapi.Schema(type=openapi.TYPE_OBJECT, properties={})
            }
        )),
        404: openapi.Response(description='Not Found'),
        500: openapi.Response(description='Internal Server Error')
    }
)
@api_view(['DELETE'])
def delete_player_friend(request, id):
    try:
        friend = Friends.objects.get(id=id)
        friend.delete()
        return JsonResponse({'message': "Korisnik uspjesno obrisan iz prijatelja"}, status=status.HTTP_200_OK)
    except Friends.DoesNotExist:
        return JsonResponse({'status': False, 'message': 'Korisnik nije pronađen'}, status=status.HTTP_404_NOT_FOUND)


#
# @swagger_auto_schema(
#     method='get',
#     responses={
#         200: "OK",
#         404: "User not found"
#     }
# )
# @api_view(['GET'])
# def sort_player_invitations(request, id):
#     try:
#         data = request.GET
#         sorting_column = data.get('column')
#         sorting_order = data.get('order')
#         invite_status = data.get('status')
#         if sorting_order == 'asc':
#             sorted_queryset = list(Invitations.objects.filter(recipient_id=id, status=invite_status)
#                                    .values('id', 'sender__username', 'time_sent', 'status', 'details', 'type')
#                                    .order_by(sorting_column))
#         else:
#             sorted_queryset = list(Invitations.objects.filter(recipient_id=id, status=invite_status)
#                                    .values('id', 'sender__username', 'time_sent', 'status', 'details', 'type')
#                                    .order_by('-' + sorting_column))
#
#         return JsonResponse(sorted_queryset, safe=False, status=status.HTTP_200_OK)
#     except:
#         return JsonResponse({"message": "Korisnik nije pronađen"}, status=status.HTTP_404_NOT_FOUND)
#

@swagger_auto_schema(
    method='get',
    tags=['Player'],
    responses={
        200: "OK",
        404: "User not found"
    }
)
@api_view(['GET'])
def sort_player_history(request, id):
    try:
        data = request.GET
        sorting_column = data.get('column')
        sorting_order = data.get('order')
        player_teams = list(TeamMembers.objects.filter(user_id_id=id).values_list('team_id_id', flat=True))
        if sorting_order == 'asc':
            sorted_queryset = list(Games.objects.filter(team_id__in=player_teams)
                                   .values('id', 'hall_name', 'status', 'time_appointed',
                                           team_name=F('team_id__permanentteams__team_name'))
                                   .order_by(sorting_column))
        else:
            sorted_queryset = list(Games.objects.filter(team_id__in=player_teams)
                                   .values('id', 'hall_name', 'status', 'time_appointed',
                                           team_name=F('team_id__permanentteams__team_name'))
                                   .order_by('-' + sorting_column))

        return JsonResponse(sorted_queryset, safe=False, status=status.HTTP_200_OK)
    except Games.DoesNotExist:
        return JsonResponse({"message": "Korisnik nije pronađen"}, status=status.HTTP_404_NOT_FOUND)


@swagger_auto_schema(
    method='get',
    tags=['Player'],
    responses={
        200: "OK",
        404: "User not found"
    }
)
@api_view(['GET'])
def sort_player_friends(request, player_id):
    try:
        data = request.GET
        sorting_column = data.get('column')
        sorting_order = data.get('order')
        if sorting_order == 'asc':
            sorted_queryset = list(Friends.objects.filter(user1_id=player_id)
                                   .values('id', 'user2__username')
                                   .order_by(sorting_column))
        else:
            sorted_queryset = list(Friends.objects.filter(user1_id=player_id)
                                   .values('id', 'user2__username')
                                   .order_by('-' + sorting_column))

        return JsonResponse(sorted_queryset, safe=False, status=status.HTTP_200_OK)
    except Friends.DoesNotExist:
        return JsonResponse({"message": "Korisnik nije pronađen"}, status=status.HTTP_404_NOT_FOUND)


@swagger_auto_schema(
    method='put',
    tags=['Invitations'],
    operation_id='UpdateInvitationStatus',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'status': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='The status to update the invitation'
            ),
        },
        required=['status']
    ),
    responses={
        200: "OK",  # Replace with your 200 response schema
        404: "Not found",  # Replace with your 404 response schema
    }
)
@api_view(['PUT'])
def update_invitation_status(request, invitation_id):
    try:
        data = request.data
        invitations = Invitations.objects.get(id=invitation_id)
        invitations.status = data.get('status')
        invitations.save()
        return JsonResponse({'status': True, 'message': 'Status uspješno promijenjen'}, status=status.HTTP_200_OK)
    except Invitations.DoesNotExist:
        return JsonResponse({'status': False, 'message': 'Korisnik nije pronađen'}, status=status.HTTP_404_NOT_FOUND)


@swagger_auto_schema(
    method='get',
    tags=['Player'],
    manual_parameters=[
        openapi.Parameter('user_id', openapi.IN_PATH,
                          description='User id', type=openapi.TYPE_STRING),
    ]
)
@api_view(['GET'])
def get_player_games(request, user_id):
    try:
        player_teams = list(TeamMembers.objects.filter(user_id_id=user_id).values_list('team_id_id', flat=True))
        teams = list(Games.objects.filter(team_id__in=player_teams)
                     .values('id', 'hall_name', 'status', 'time_appointed',
                             team_name=F('team_id__permanentteams__team_name')))
        return JsonResponse({'teams': teams}, status=status.HTTP_200_OK)
    except TeamMembers.DoesNotExist:
        return JsonResponse({"message": "Korisnik nije pronadjen"}, status=status.HTTP_404_NOT_FOUND)
    except Games.DoesNotExist:
        return JsonResponse({"message": "Games nije pronadjen"}, status=status.HTTP_404_NOT_FOUND)
