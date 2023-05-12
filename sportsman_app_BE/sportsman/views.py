from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
import json
from .models import *


# Create your views here.

@api_view(['POST'])
def registrationPlayer(request):
    name = request.data.get('name')
    surname = request.data.get('surname')
    username = request.data.get('username')
    email = request.data.get('email')
    phone = request.data.get('phone')
    password = request.data.get('password')
    repeatedPassword = request.data.get('repeatedPassword')
    city = request.data.get('city')
    age = request.data.get('age')
    sports = request.data.get('interests')
    if not sports:
        interests = ""
    else:
        interests = json.dumps({"interests": sports})
    user = User.objects.filter(email=email)
    if password != repeatedPassword:
        return JsonResponse({'status': False, 'message': "Lozinke se ne podudaraju"}, status=400)
    elif len(user) > 0:
        return JsonResponse({'status': False, 'message': "Email je već registrovan."}, status=400)
    else:
        User.objects.create(name=name, surname=surname, username=username, email=email,
                            tel_number=phone, city=city, age=age, interests=interests,
                            password=make_password(password))
        return JsonResponse({'status': True, 'message': "Uspješno ste se registrovali."}, status=201)

@api_view(['POST'])
def registrationOwner(request):
    name = request.data.get('name')
    surname = request.data.get('surname')
    username = request.data.get('username')
    email = request.data.get('email')
    phone = request.data.get('phone')
    password = request.data.get('password')
    repeatedPassword = request.data.get('repeatedPassword')
    city = request.data.get('city')
    capacity = request.data.get('capacity')
    street = request.data.get('street')
    streetNumber = request.data.get('streetNumber')
    type = request.data.get('type')
    location = json.dumps({"city": city, "street": street, "streetNumber": streetNumber})
    owner = Owner.objects.filter(email=email)

    if password != repeatedPassword:
        return JsonResponse({'status': False, 'message': "Lozinke se ne podudaraju"}, status=400)
    elif len(owner) > 0:
        return JsonResponse({'status': False, 'message': "Email je već registrovan."}, status=400)
    else:
        Owner.objects.create(name=name, surname=surname, username=username, email=email,
                            tel_number=phone, location=location, capacity=capacity, type=type,
                            password=make_password(password))
        return JsonResponse({'status': True, 'message': "Uspješno ste se registrovali."}, status=201)


@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    if (User.objects.filter(email=email).exists()) == False:
        return JsonResponse({'status': 404, 'message': 'Korisnik sa unesenim emailom nije registrovan'}, status=404)
    elif check_password(password, User.objects.get(email=email).password) == False:
        return JsonResponse({'status': 400, 'message': 'Pogrešni kredencijali'}, status=400)
    else:
        user = list(User.objects.filter(email=email).values(
            'name', 'surname', 'email', 'phone', 'username', 'typeOfUser'))
        return JsonResponse(user, safe=False)
