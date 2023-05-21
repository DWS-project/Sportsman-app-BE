import json

from django.db.models import Q
from django.forms import model_to_dict
from django.http import JsonResponse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from django.contrib.auth.hashers import make_password, check_password
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.response import Response


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
            'repeated_password': openapi.Schema(type=openapi.TYPE_STRING, description='The repeated password field'),
            'city': openapi.Schema(type=openapi.TYPE_STRING, description='The city field'),
            'age': openapi.Schema(type=openapi.TYPE_INTEGER, description='The age field'),
            'sports': openapi.Schema(type=openapi.TYPE_STRING, description='The interests field'),
        },
        required=['name', 'surname', 'username', 'email', 'tel_number', 'password', 'repeated_password', 'city', 'age',
                  'sports']

    )
)
@api_view(['POST'])
def registration_player(request):
    name = request.data.get('name')
    surname = request.data.get('surname')
    username = request.data.get('username')
    email = request.data.get('email')
    tel_number = request.data.get('tel_number')
    password = request.data.get('password')
    repeated_password = request.data.get('repeatedPassword')
    city = request.data.get('city')
    age = request.data.get('age')
    sports = request.data.get('interests')
    if not sports:
        interests = ""
    else:
        interests = json.dumps({"interests": sports})
    user = User.objects.filter(email=email)
    if password != repeated_password:
        return JsonResponse({'status': False, 'message': "Lozinke se ne podudaraju"}, status=400)
    elif len(user) > 0:
        return JsonResponse({'status': False, 'message': "Email je već registrovan."}, status=400)
    else:
        User.objects.create(name=name, surname=surname, username=username, email=email,
                            tel_number=tel_number, city=city, age=age, interests=interests,
                            password=make_password(password),
                            role='renter')
        return JsonResponse({'status': True, 'message': "Uspješno ste se registrovali."}, status=201)


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
            'repeated_password': openapi.Schema(type=openapi.TYPE_STRING, description='The repeated password field'),
            'city': openapi.Schema(type=openapi.TYPE_STRING, description='The city field'),
            'capacity': openapi.Schema(type=openapi.TYPE_INTEGER, description='The capacity field'),
            'street': openapi.Schema(type=openapi.TYPE_STRING, description='The street field'),
            'streetNumber': openapi.Schema(type=openapi.TYPE_STRING, description='The street number field'),
            'type': openapi.Schema(type=openapi.TYPE_STRING, description='The type field'),
        },
        required=['name', 'surname', 'username', 'email', 'tel_number', 'password', 'repeated_password', 'city',
                  'capacity', 'street', 'streetNumber', 'type']
    )
)
@api_view(['POST'])
def registration_owner(request):
    name = request.data.get('name')
    surname = request.data.get('surname')
    username = request.data.get('username')
    email = request.data.get('email')
    tel_number = request.data.get('tel_number')
    password = request.data.get('password')
    repeated_password = request.data.get('repeatedPassword')
    city = request.data.get('city')
    capacity = request.data.get('capacity')
    street = request.data.get('street')
    street_number = request.data.get('streetNumber')
    type_of_user = request.data.get('type')
    location = json.dumps(
        {"city": city, "street": street, "streetNumber": street_number})
    owner = Owner.objects.filter(email=email)

    if password != repeated_password:
        return JsonResponse({'status': False, 'message': "Lozinke se ne podudaraju"}, status=400)
    elif len(owner) > 0:
        return JsonResponse({'status': False, 'message': "Email je već registrovan."}, status=400)
    else:
        Owner.objects.create(name=name, surname=surname, username=username, email=email,
                             tel_number=tel_number, location=location, capacity=capacity, type=type_of_user,
                             password=make_password(password))
        return JsonResponse({'status': True, 'message': "Uspješno ste se registrovali."}, status=201)


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

    user = User.objects.get(email=email)

    if user is not None:
        is_password_valid = check_password(password, user.password)

        if is_password_valid:
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh)
            user.access_token = access_token

            response.set_cookie(
                "Authentication", access_token, 86400, httponly=True)
            response.data = {"user": {"id": user.id,
                                      "email": user.email, "role": user.role}}
            response.message = "Login successfully"

            return response
        else:
            return Response({"message": "Invalid username or password!!",
                             "data": {},
                             }, status=status.HTTP_404_NOT_FOUND)

    else:
        return Response({"message": "Invalid username or password!!",
                         "data": {},
                         }, status=status.HTTP_404_NOT_FOUND)


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

    response.data = {"message": "Logged out successfully"}
    return response

@api_view(['GET'])
def landing_page(request):
    selected_price = request.GET.get('price')
    selected_city = request.GET.get('city')
    selected_sports = request.GET.getlist('sports[]')
    selected_type = request.GET.getlist('type[]')
    selected_date = request.GET.get('date')
    selected_time = request.GET.get('time')
    search_text = request.GET.get('searchText')
    sort_type = request.GET.get('sort_type')
    sort_price = request.GET.get('sort_price')

    queryset = SportHall.objects.all()

    # Apply filters based on selected options
    if selected_city:
        queryset = queryset.filter(city=selected_city)

    if selected_type:
        queryset = queryset.filter(type__in=selected_type)

    if selected_price:
        queryset = queryset.filter(price__lte=selected_price)

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

    filtered_items = []
    for item in queryset:
        sports_string = item.sports  # Get the string representation of the sports object
        sports_list = json.loads(sports_string)  # Convert the string to a Python object (dictionary or list)
        if any(sport in sports_list['sports'] for sport in selected_sports):
            filtered_items.append(model_to_dict(item))

    print(filtered_items)
    return JsonResponse({'data': filtered_items})
