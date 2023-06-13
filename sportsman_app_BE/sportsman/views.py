import json
from datetime import timedelta
#import firebase_admin
from django.db.models import F
from django.http import JsonResponse
from django.utils import timezone
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from django.core.exceptions import ObjectDoesNotExist
import json
from os import environ
import jwt
from django.conf import settings


from django.forms import model_to_dict
from django.http import JsonResponse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
import json

from rest_framework.response import Response

from django.core.mail import EmailMessage

from django.contrib.auth.hashers import make_password, check_password

from django.conf import settings
from .helpers import send_confirmation_email
from .models import *
from django.utils.crypto import get_random_string
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.response import Response
from django.core.mail import send_mail
#from firebase_admin import storage
from django.core import serializers


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
            'email_confirmed': False
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
            'streetNumber': openapi.Schema(type=openapi.TYPE_STRING, description='The street number field'),
            'type': openapi.Schema(type=openapi.TYPE_STRING, description='The type field'),
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
    type_of_user = data.get('type')
    location = json.dumps(
        {"city": city, "street": street, "streetNumber": street_number})
    owner = Owner.objects.filter(email=email)

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
            'location': location,
            'capacity': capacity,
            'type': type_of_user,
            'password': make_password(password),
            'confirmation_token': token,
            'email_confirmed': False
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

    if (User.objects.filter(email=email).exists() == True):
        user = User.objects.get(email=email)
        is_password_valid = check_password(password, user.password)
        if is_password_valid:
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh)
            user.access_token = access_token
            user_picture = None
            if user.picture:
                user_picture = user.picture
            response.set_cookie(
                "Authentication", access_token, 86400, httponly=True)

            response.data = {"user": {"id": user.id,
                                      "email": user.email, "username": user.username,
                                      "tel_number": user.tel_number, "age": user.age, "city": user.city,
                                      "interests": user.interests,
                                      "name": user.name, "surname": user.surname}}
            response.message = "Login successfully"

            return response
        else:
            return Response({"message": "Invalid username or password!!",
                             "data": {},
                             }, status=status.HTTP_400_BAD_REQUEST)

    elif (Owner.objects.filter(email=email).exists() == True):
        owner = Owner.objects.get(email=email)
        is_password_valid = check_password(password, owner.password)

        if is_password_valid:
            refresh = RefreshToken.for_user(owner)
            access_token = str(refresh)
            owner.access_token = access_token
            owner_picture = None
            if owner.picture:
                owner_picture = owner.picture
            response.set_cookie(
                "Authentication", access_token, 86400, httponly=True)

            response.data = {"owner": {"id": owner.id,
                                       "email": owner.email, "username": owner.username,
                                       "tel_number": owner.tel_number, "location": owner.location,
                                       "capacity": owner.capacity, "name": owner.name, "surname": owner.surname,
                                       "picture": owner_picture}}
            response.message = "Login successfully"

            return response
    else:
        return Response({"message": "Invalid username or password!!",
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
    response = Response()

    if request.user.is_authenticated:
        request.user.access_token = None
        request.user.save()

    response.delete_cookie("Authentication")
    return Response({"message": "Logged out successfully.",
                     "data": {},
                     }, status=status.HTTP_200_OK)

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
    type = request.GET.getlist('type[]')
    date = request.GET.get('date')
    time = request.GET.get('time')
    search_text = request.GET.get('searchText')
    sort_type = request.GET.get('sort_type')
    sort_price = request.GET.get('sort_price')

    queryset = SportHall.objects.all()

    if city:
        queryset = queryset.filter(city=city)

    if type:
        queryset = queryset.filter(type__in=type)

    if price:
        queryset = queryset.filter(price__lte=price)

    if search_text:
        queryset = queryset.filter(title__icontains=search_text)

    if sort_type:
        if sort_type == 'Unutrašnji':
            queryset = queryset.order_by('type')
        elif sort_type == 'Vanjski':
            queryset = queryset.order_by('-type')

    if sort_price:
        if sort_price == 'Najjeftiniji':
            queryset = queryset.order_by('price')
        elif sort_price == 'Najskuplji':
            queryset = queryset.order_by('-price')

    if date and time:
        reservations = Reservations.objects.filter(date=date, time_from__lte=time, time_to__gte=time)
        reserved_hall_ids = reservations.values_list('sport_hall_id', flat=True)
        queryset = queryset.exclude(id__in=reserved_hall_ids)

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
    if User.objects.filter(email=email).exists() == False & Owner.objects.filter(email=email).exists() == False:
        return JsonResponse({'status': False, 'message': 'Korisnik sa unesenim emailom nije registrovan'},
                            status=status.HTTP_404_NOT_FOUND)
    else:
        if User.objects.filter(email=email).exists() == True:
            password = get_random_string(8)
            user = User.objects.get(email=email)
            user.password = make_password(password)
            user.save()
            send_mail(
                'PROMJENA LOZINKE',
                'Vaša nova lozinka je ' + password,
                'redroseb1206@gmail.com',
                [email],
                fail_silently=False)
            return JsonResponse({'status': True, 'message': 'Nova lozinka Vam je poslana na ' + email},
                                status=status.HTTP_200_OK)
        elif (Owner.objects.filter(email=email).exists() == True):
            password = get_random_string(8)
            owner = Owner.objects.get(email=email)
            owner.password = make_password(password)
            owner.save()
            send_mail(
                'PROMJENA LOZINKE',
                'Vaša nova lozinka je ' + password,
                'redroseb1206@gmail.com',
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
    users = list(User.objects.values(
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
    owners = list(Owner.objects.values(
        'id', 'name', 'surname', 'location', 'username', 'capacity', 'picture', 'tel_number'))
    return JsonResponse(owners, safe=False, status=status.HTTP_200_OK)


@swagger_auto_schema(
    tags=['Sport Hall'],
    method='get',
    responses={
        200: "OK",
    }
)
@api_view(['GET'])
def get_all_sport_halls(request):
    sport_halls = list(SportHall.objects.values(
        'title', 'city', 'address', 'description', 'status', 'price', 'pictures', 'owner_id', 'id'))
    return JsonResponse(sport_halls, safe=False, status=status.HTTP_200_OK)

@swagger_auto_schema(
    method='get',
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
    method='put',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'new_password': openapi.Schema(type=openapi.TYPE_STRING, description='The new password field'),
            'new_repeated_password': openapi.Schema(type=openapi.TYPE_STRING, description='The new repeated password field'),
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
def update_player_password(request, id):
    try:
        user = User.objects.get(id=id)
        data = request.data
        old_password = data.get('oldPassword')
        new_password = data.get('newPassword')
        new_repeated_password = data.get('newRepeatedPassword')
        is_password_valid = check_password(old_password, user.password)
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
        bucket = ''#storage.bucket()
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
    responses={
        200: "OK",
        404: "User not found"
    }
)
@api_view(['GET'])
def get_owner_data(request, id):
    try:
        owner = list(Owner.objects.filter(id=id).values())
        return JsonResponse(owner, safe=False, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return JsonResponse({"error": "Korisnik nije pronađen"}, status=status.HTTP_404_NOT_FOUND)


@swagger_auto_schema(
    method='put',
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
        owner = Owner.objects.get(id=id)
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
    method='put',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'new_password': openapi.Schema(type=openapi.TYPE_STRING, description='The new password field'),
            'new_repeated_password': openapi.Schema(type=openapi.TYPE_STRING, description='The new repeated password field'),
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
def update_owner_password(request, id):
    try:
        owner = Owner.objects.get(id=id)
        data = request.data
        old_password = data.get('oldPassword')
        new_password = data.get('newPassword')
        new_repeated_password = data.get('newRepeatedPassword')
        is_password_valid = check_password(old_password, owner.password)
        if is_password_valid:
            if new_password == new_repeated_password:
                owner.password = make_password(new_password)
                owner.save()
                return JsonResponse({'status': True, 'message': 'Podatci uspješno promijenjeni'},
                                    status=status.HTTP_200_OK)
            else:
                return JsonResponse({'status': False, 'message': 'Lozinke se ne podudaraju'},
                                    status=status.HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse({'success': False, 'message': 'Pogrešna lozinka'}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return JsonResponse({'success': False, 'message': 'Korisnik nije pronađen'}, status=status.HTTP_404_NOT_FOUND)

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
        SportHall.objects.create(title=title, city=city, address=address,
                                 description=description, status=sport_hall_status, price=price, capacity=capacity,
                                 owner_id_id=owner_id, pictures=pictures)
        return JsonResponse({'data': {title, city, address, description, price}, 'message': 'Uspješno kreiran novi teren.'},
                        status=status.HTTP_200_OK)
    else:
        return JsonResponse({'data': {}, 'message': 'Došlo je do greške.'}, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    tags=['Sport Hall'],
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'owner_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the owner'),
            'sporthall_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the sport hall'),
        },
        required=['owner_id', 'sporthall_id'],
        example={
            'owner_id': 1,
            'sporthall_id': 2
        }
    ),
    responses={
        200: openapi.Response(description='Success', schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'status': openapi.Schema(type=openapi.TYPE_BOOLEAN,
                                         description='Indicates if the request was successful'),
                'message': openapi.Schema(type=openapi.TYPE_STRING, description='A message indicating the result')
            }
        )),
        404: "Not Found",
        500: "Internal Server Error"
    }
)
@api_view(['POST'])
def get_sport_hall(request):
    data = request.data
    owner_id = data.get('owner_id')
    sporthall_id = data.get('sporthall_id')
    owner = Owner.objects.get(id=owner_id)
    sporthall = SportHall.objects.get(id=sporthall_id)
    array_of_sporthalls = [owner, sporthall]
    try:
        sporthalls_of_owner = Owner_SportHall.objects.filter(
            owner_id_id=owner_id)
        for sport_hall in sporthalls_of_owner:
            if (int(sport_hall.owner_id_id) == int(owner_id)):
                array_of_sporthalls.append(sport_hall)
                break
    except:
        obj = serializers.serialize('json', array_of_sporthalls)
        return JsonResponse({'data': json.loads(obj)}, status=status.HTTP_404_NOT_FOUND)
    obj = serializers.serialize('json', array_of_sporthalls)
    return JsonResponse({'data': json.loads(obj)}, status=status.HTTP_200_OK)

@swagger_auto_schema(
    tags=['Sport Hall'],
    method='get',
    manual_parameters=[
        openapi.Parameter('sporthall_id', openapi.IN_QUERY,
                          description='ID of the sport hall', type=openapi.TYPE_INTEGER),
    ],
    responses={
            200: openapi.Response(description='Success', schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'status': openapi.Schema(type=openapi.TYPE_BOOLEAN,
                                             description='Indicates if the request was successful'),
                    'data': openapi.Schema(type=openapi.TYPE_OBJECT, description='Object containing sport hall data')
                }
            )),
            404: "Not Found",
            500: "Internal Server Error"
        }
)
@api_view(['GET'])
def get_sport_hall_user(request):
    sporthall_id = request.GET.get('id')
    sporthall = SportHall.objects.get(id=sporthall_id)
    sporthall_data = model_to_dict(sporthall)
    if sporthall:
        return JsonResponse({'status': True, 'data': sporthall_data}, status=status.HTTP_200_OK)
    else:
        return JsonResponse({'status': False, 'data': {}}, status=status.HTTP_404_NOT_FOUND)

@swagger_auto_schema(
    tags=['Reservation'],
    method='get',
    manual_parameters=[
        openapi.Parameter('sporthall_id', openapi.IN_QUERY,
                          description='ID of the sport hall', type=openapi.TYPE_INTEGER),
    ],
    responses={
            200: openapi.Response(description='Success', schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'status': openapi.Schema(type=openapi.TYPE_BOOLEAN,
                                             description='Indicates if the request was successful'),
                    'data': openapi.Schema(type=openapi.TYPE_OBJECT,
                                           description='Object containing all reservations for specific sport hall')
                }
            )),
            500: "Internal Server Error"
        }
)
@api_view(['GET'])
def get_sport_hall_reservations(request):
    sporthall_id = request.GET.get('id')
    try:
        reservations = list(Reservations.objects.filter(sport_hall_id_id=sporthall_id).values())
        return JsonResponse({'status': True, 'data': reservations}, status=status.HTTP_200_OK)
    except Reservations.DoesNotExist:
        return JsonResponse({'status': False, 'data': {}})

@swagger_auto_schema(
    tags=['Player'],
    method='get',
    manual_parameters=[
        openapi.Parameter('user_id', openapi.IN_QUERY,
                          description='ID of the user', type=openapi.TYPE_INTEGER),
    ],
    responses={
            200: openapi.Response(description='Success', schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'status': openapi.Schema(type=openapi.TYPE_BOOLEAN,
                                             description='Indicates if the request was successful'),
                    'data': openapi.Schema(type=openapi.TYPE_OBJECT,
                                           description='Object containing all friends of some player')
                }
            )),
            500: "Internal Server Error"
        }
)
@api_view(['GET'])
def get_friends(request):
    user_id = request.GET.get('id')
    friend_ids = []
    friends_user1 = Friends.objects.filter(user1=user_id).values_list("user2_id", flat=True)
    friend_ids.extend(friends_user1)

    friends_user2 = Friends.objects.filter(user2=user_id).values_list("user1_id", flat=True)
    friend_ids.extend(friends_user2)

    friend_ids = list(set(friend_ids))
    friends_data = User.objects.filter(id__in=friend_ids).values()
    friends_data_list = list(friends_data)
    if friend_ids:
        return JsonResponse({'status': True, 'data': friends_data_list}, status=status.HTTP_200_OK)
    else:
        return JsonResponse({'status': False, 'data': {}})

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
        500: openapi.Response(description='Internal Server Error')
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
    method='post',
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
        404: "Not Found",
        500: "Internal Server Error"
    }
)
@api_view(['POST'])
def change_sporthall_status(request):
    data = request.data
    sporthall_id = data.get('sporthall_id')
    status = data.get('status')

    try:
        sporthall = SportHall.objects.get(id=sporthall_id)
        sporthall.status = status
        sporthall.save()
        obj = serializers.serialize('json', sporthall)
        return JsonResponse({'data': json.loads(obj)}, status=200)
    except:
        return JsonResponse({'data': {}}, status=400)

@api_view(['POST'])
def create_team(request):
    name = request.data.get('name')
    lead_id = request.data.get('id')
    user = User.objects.get(id=lead_id)
    team_lead = Team.objects.create(team_lead_id_id=lead_id)
    PermanentTeams.objects.create(team_name=name, team_id_id=team_lead.id)
    return JsonResponse({'success': True, 'message': 'Uspješno kreiran tim'}, status=201)


@api_view(['GET'])
def get_perm_teams(request):
    id = request.GET.get('id')
    list_of_teams = PermanentTeams.objects.filter(team_id__team_lead_id_id=id)
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


@api_view(['DELETE'])
def delete_team(request):
    team_id = request.GET.get('id')
    team = PermanentTeams.objects.get(id=team_id)
    team.delete()
    return JsonResponse({'message': "Uspješno uklonjen tim.", 'data': {}}, status=status.HTTP_200_OK)


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

    Invitations.objects.create(recipient_id=user.id,sender_id=lead_id, time_sent=formatted_time,
    status=0, details=details_json)
    response_data = {
        'message': 'Invitation sent successfully',
        'memberName': name,

    }

    return JsonResponse(response_data)

@api_view(['DELETE'])
def delete_team_member(request):
    email = request.GET.get('email')
    user = User.objects.get(email=email)
    user_id = user.id
    team_id = request.GET.get('teamId')

    team_member = TeamMembers.objects.get(user_id_id=user_id, team_id_id=team_id)
    team_member.delete()

    return JsonResponse({'message': "Uspješno uklonjen član tim.", 'data': {}}, status=status.HTTP_200_OK)

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
        return Response({'message': 'Email confirmed successfully'})

    except jwt.ExpiredSignatureError:
        return Response({'message': 'Token has expired'})
    except (jwt.DecodeError, User.DoesNotExist):
        return Response({'message': 'Invalid token'})


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
        {'message': 'Poštovani, hvala vam što ste nas kontaktirali! Odgovorit ćemo vam u što skorijem roku.'}, status=status.HTTP_200_OK)



@swagger_auto_schema(
    method='get',
    responses={
        200: "OK",
        404: "User not found"
    }
)
@api_view(['GET'])
def get_player_invitations(request, id):
    try:
        invitations = list(Invitations.objects.filter(recipient_id=id)
                       .values('id', 'sender__username', 'time_sent', 'status', 'details', 'type'))
        return JsonResponse(invitations, safe=False, status=status.HTTP_200_OK)
    except:
        return JsonResponse({"message": "Korisnik nije pronadjen"}, status=status.HTTP_404_NOT_FOUND)


@swagger_auto_schema(
    method='get',
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
    except:
        return JsonResponse({"message": "Korisnik nije pronadjen"}, status=status.HTTP_404_NOT_FOUND)

@swagger_auto_schema(
    tags=['Reservation'],
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING, description='Name'),
            'surname': openapi.Schema(type=openapi.TYPE_STRING, description='Surname'),
            'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email'),
            'phone': openapi.Schema(type=openapi.TYPE_STRING, description='Phone'),
            'date': openapi.Schema(type=openapi.TYPE_STRING, description='Date'),
            'from_time': openapi.Schema(type=openapi.TYPE_STRING, description='Time from'),
            'to_time': openapi.Schema(type=openapi.TYPE_STRING, description='Time to'),
            'user_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the player'),
            'team_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the team'),
            'reservation_type': openapi.Schema(type=openapi.TYPE_STRING, description='Type of reservation'),
            'team_members': openapi.Schema(type=openapi.TYPE_STRING, description='Members of team'),
            'sport_hall_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the sport hall'),
        },
        required=['name', 'surname', 'email', 'phone', 'date', 'from_time', 'to_time', 'user_id',
                  'team_id', 'reservation_type', 'team_members', 'sport_hall_id'],
        example={
            'name': 'John Doe',
            'email': 'johndoe@example.com',
            'phone': '061123456',
            'date': '2023-06-11',
            'from_time': '10:00',
            'to_time': '12:30',
            'user_id': 1,
            'team_id': 0,
            'reservation_type': 'reservation',
            'team_members': '',
            'sport_hall_id': 2
            },
    ),
    responses={
        200: openapi.Response(
            description='Success',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'message': openapi.Schema(type=openapi.TYPE_STRING, description='A message indicating the result'),
                    'data': openapi.Schema(type=openapi.TYPE_OBJECT, properties={})
                })),
        404: openapi.Response(description='Not Found'),
        500: openapi.Response(description='Internal Server Error')
    }
)
@api_view(['POST'])
def reservation(request):
    try:
        data = request.data
        name = data.get('name')
        surname = data.get('surname')
        email = data.get('email')
        phone = data.get('phone')
        date = data.get('date')
        time_from = data.get('fromTime')
        time_to = data.get('toTime')
        sport_hall_id = data.get('sportHallId')
        user_id = data.get('userId')
        team_id = data.get('teamId')
        reservation_type = data.get('type')
        team_members = data.get('teamMembers')

        if reservation_type not in ['temporary', 'permanent', 'reservation']:
            raise ValueError('Invalid reservation type.')

        if reservation_type == 'temporary':
            team = Team.objects.create(team_lead_id_id=user_id)
            team_id = team.id
            for member in team_members:
                TeamMembers.objects.create(user_id_id=member['id'], team_id_id=team.id)

        reservation = Reservations.objects.create(name=name, surname=surname, email=email, tel_number=phone,
                                                  date=date, time_from=time_from, time_to=time_to, team_id=team_id,
                                                  sport_hall_id_id=sport_hall_id, user_id=user_id)
        if reservation:
            return JsonResponse({'status': True}, status=status.HTTP_200_OK)
        else:
            return JsonResponse({'status': False, 'message': 'Failed to create reservation.'},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except ValueError as ve:
        return JsonResponse({'status': False, 'message': str(ve)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JsonResponse({'status': False, 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    tags=['Player'],
    method='get',
    manual_parameters=[
        openapi.Parameter('user_id', openapi.IN_QUERY,
                          description='ID of the user', type=openapi.TYPE_INTEGER),
    ],
    responses={
            200: openapi.Response(description='Success', schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'status': openapi.Schema(type=openapi.TYPE_BOOLEAN,
                                             description='Indicates if the request was successful'),
                    'data': openapi.Schema(type=openapi.TYPE_OBJECT,
                                           description='Object containing all teams where specific user is team lead')
                }
            )),
            500: "Internal Server Error"
        }
)
@api_view(['GET'])
def get_permanent_teams(request):
    user_id = request.GET.get('id')
    try:
        teams = list(PermanentTeams.objects.filter(team_id__team_lead_id_id=user_id).values())
        return JsonResponse({'status': True, 'data': teams}, status=status.HTTP_200_OK)
    except PermanentTeams.DoesNotExist:
        return JsonResponse({'status': False, 'data': {}})

@swagger_auto_schema(
    tags=['Player'],
    method='get',
    manual_parameters=[
        openapi.Parameter('searchText', openapi.IN_QUERY,
                          description='Text of the search', type=openapi.TYPE_STRING),
    ],
    responses={
            200: openapi.Response(description='Success', schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'status': openapi.Schema(type=openapi.TYPE_BOOLEAN,
                                             description='Indicates if the request was successful'),
                    'data': openapi.Schema(type=openapi.TYPE_OBJECT,
                                           description='Object containing all players whose '
                                                       'usernames contain provided text')
                }
            )),
            500: "Internal Server Error"
        }
)

@api_view(['GET'])
def get_users(request):
    search_text = request.GET.get('searchText')
    try:
        users = list(User.objects.filter(username__icontains=search_text).values())
        return JsonResponse({'status': True, 'data': users}, status=status.HTTP_200_OK)
    except PermanentTeams.DoesNotExist:
        return JsonResponse({'status': False, 'data': {}})

@swagger_auto_schema(
    tags=['Invitation'],
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'sender_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Name'),
            'recipient_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Surname'),
            'sport_hall_id': openapi.Schema(type=openapi.TYPE_STRING, description='Email'),
            'sport_hall_title': openapi.Schema(type=openapi.TYPE_STRING, description='Phone'),
        },
        required=['sender_id', 'recipient_id', 'sport_hall_id', 'sport_hall_title', 'date'],
    ),
    responses={
        200: openapi.Response(description='Success', schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'status': openapi.Schema(type=openapi.TYPE_BOOLEAN,
                                         description='Indicates if the request was successful'),
                'data': openapi.Schema(type=openapi.TYPE_OBJECT,
                                       description='Object containing created invitation')
            }
        )),
        500: 'Internal Server Error'
    }
)

@api_view(['POST'])
def invite_temporary_team(request):
    sender_id = request.data.get('senderId')
    recipient_id = request.data.get('recipientId')
    sport_hall_id = request.data.get('sportHallId')
    sport_hall_title = request.data.get('sportHallTitle')
    current_time = timezone.localtime(timezone.now())
    formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S')
    details_data = {
        'sport_hall_id': sport_hall_id,
        'sport_hall_title': sport_hall_title,
    }
    details_json = json.dumps(details_data)
    invite = Invitations.objects.create(sender_id=sender_id, recipient_id=recipient_id, time_sent=formatted_time,
                                        status=0, details=details_json, type='Temporary')
    invite_data = {
        'model': 'sportsman.invitations',
        'fields': {
            'id': invite.id,
            'sender': invite.sender_id,
            'recipient': invite.recipient_id,
            'status': invite.status,
            'details': invite.details,
            'type': invite.type,
            'time_sent': invite.time_sent,
        },
    }

    invite_json = json.dumps(invite_data)
    deserialized_invite = json.loads(invite_json)

    return JsonResponse({'status': True, 'data': deserialized_invite})


@swagger_auto_schema(
    tags=['Invitation'],
    method='delete',
    manual_parameters=[
        openapi.Parameter('invite_id', openapi.IN_QUERY,
                          description='ID of the invitation', type=openapi.TYPE_INTEGER),
    ],
    responses={
            200: openapi.Response(description='Success', schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'status': openapi.Schema(type=openapi.TYPE_BOOLEAN,
                                             description='Indicates if the request was successful'),
                }
            )),
            500: "Internal Server Error"
        }
)

@api_view(['DELETE'])
def remove_invite_temporary_team(request):
    invite_id = request.data.get('id')
    print(invite_id)
    invite = Invitations.objects.get(id=invite_id)
    invite.delete()
    return JsonResponse({'status': True}, status=status.HTTP_200_OK)

@swagger_auto_schema(
    tags=['Player'],
    method='get',
    manual_parameters=[
        openapi.Parameter('recipients_ids', openapi.IN_QUERY,
                          description='IDs of invited players', type=openapi.TYPE_STRING),
    ],
    responses={
            200: openapi.Response(description='Success', schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'status': openapi.Schema(type=openapi.TYPE_BOOLEAN,
                                             description='Indicates if the request was successful'),
                    'data': openapi.Schema(type=openapi.TYPE_OBJECT,
                                             description='Object containing invited players')
                }
            )),
            500: "Internal Server Error"
        }
)
@api_view(['GET'])
def get_invited_users(request):
    recipients_ids = request.GET.get('recipientsIds')
    recipients_ids = recipients_ids.split(',') if recipients_ids else []
    try:
        recipients = User.objects.filter(id__in=recipients_ids).values()
        recipients = list(recipients)
        return JsonResponse({'status': True, 'data': recipients}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return JsonResponse({'status': False, 'data': {}})
@api_view(['DELETE'])
def delete_player_friend(request, id):
    try:
        friend = Friends.objects.get(id=id)
        friend.delete()
        return JsonResponse({'message': "Korisnik uspjesno obrisan iz prijatelja"}, status=status.HTTP_200_OK)
    except Friends.DoesNotExist:
        return JsonResponse({'status': False, 'message': 'Korisnik nije pronađen'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(str(e))
        return JsonResponse({'status': False, 'message': 'Greška na serveru'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@swagger_auto_schema(
    method='get',
    responses={
        200: "OK",
        404: "User not found"
    }
)
@api_view(['GET'])
def sort_player_invitations(request, id):
    try:
        data = request.GET
        sorting_column = data.get('column')
        sorting_order = data.get('order')
        invite_status = data.get('status')
        if sorting_order == 'asc':
            sorted_queryset = list(Invitations.objects.filter(recipient_id=id, status=invite_status)
                               .values('id', 'sender__username', 'time_sent', 'status', 'details', 'type')
                               .order_by(sorting_column))
        else:
            sorted_queryset = list(Invitations.objects.filter(recipient_id=id, status=invite_status)
                               .values('id', 'sender__username', 'time_sent', 'status', 'details', 'type')
                               .order_by('-' + sorting_column))

        return JsonResponse(sorted_queryset, safe=False, status=status.HTTP_200_OK)
    except:
        return JsonResponse({"message": "Korisnik nije pronađen"}, status=status.HTTP_404_NOT_FOUND)


@swagger_auto_schema(
    method='get',
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
    except:
        return JsonResponse({"message": "Korisnik nije pronađen"}, status=status.HTTP_404_NOT_FOUND)


@swagger_auto_schema(
    method='get',
    responses={
        200: "OK",
        404: "User not found"
    }
)
@api_view(['GET'])
def sort_player_friends(request, id):
    try:
        data = request.GET
        sorting_column = data.get('column')
        sorting_order = data.get('order')
        if sorting_order == 'asc':
            sorted_queryset = list(Friends.objects.filter(user1_id=id)
                                   .values('id', 'user2__username')
                                   .order_by(sorting_column))
        else:
            sorted_queryset = list(Friends.objects.filter(user1_id=id)
                                   .values('id', 'user2__username')
                                   .order_by('-' + sorting_column))

        return JsonResponse(sorted_queryset, safe=False, status=status.HTTP_200_OK)
    except:
        return JsonResponse({"message": "Korisnik nije pronađen"}, status=status.HTTP_404_NOT_FOUND)

@swagger_auto_schema(
    method='put',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'status': openapi.Schema(type=openapi.TYPE_STRING, description='The status field'),
        },
        required=['status']
    ),
    responses={
        200: "OK",
        404: "User not found",
        500: "Internal server error",
    }
)
@api_view(['PUT'])
def update_invitation_status(request, id):
    try:
        data = request.data
        invitations = Invitations.objects.get(id=id)
        invitations.status = data.get('status')
        invitations.save()
        return JsonResponse({'status': True, 'message': 'Status uspješno promijenjen'}, status=status.HTTP_200_OK)
    except Invitations.DoesNotExist:
        return JsonResponse({'status': False, 'message': 'Korisnik nije pronađen'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(str(e))
        return JsonResponse({'status': False, 'message': 'Greška na serveru'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_player_games(request, id):
    try:
        player_teams = list(TeamMembers.objects.filter(user_id_id=id).values_list('team_id_id', flat=True))
        teams = list(Games.objects.filter(team_id__in=player_teams)
                     .values('id', 'hall_name', 'status', 'time_appointed', team_name=F('team_id__permanentteams__team_name')))
        return JsonResponse(teams, safe=False, status=status.HTTP_200_OK)
    except:
        return JsonResponse({"message": "Korisnik nije pronadjen"}, status=status.HTTP_404_NOT_FOUND)
