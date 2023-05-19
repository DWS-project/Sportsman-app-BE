import json
from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.contrib.auth.hashers import make_password, check_password
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.response import Response


# Create your views here.

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
    location = json.dumps({"city": city, "street": street, "streetNumber": street_number})
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

            response.set_cookie("Authentication", access_token, 86400, httponly=True)
            response.data = {"user": {"id": user.id, "email": user.email, "role": user.role}}
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

@api_view(['POST'])
def logout(request):
    response = Response()

    if request.user.is_authenticated:
        request.user.access_token = None
        request.user.save()

    response.delete_cookie("Authentication")

    response.data = {"message": "Logged out successfully"}
    return response
