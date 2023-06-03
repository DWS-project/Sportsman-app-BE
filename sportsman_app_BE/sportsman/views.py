import json
from datetime import timedelta

from django.http import JsonResponse
from django.utils import timezone
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from django.contrib.auth.hashers import make_password, check_password
from .models import *
from django.utils.crypto import get_random_string
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.response import Response
from django.core.mail import send_mail
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
        return JsonResponse({'status': False, 'message': "Lozinke se ne podudaraju"}, status=status.HTTP_400_BAD_REQUEST)
    elif len(user) > 0:
        return JsonResponse({'status': False, 'message': "Email je već registrovan."}, status=status.HTTP_400_BAD_REQUEST)
    else:
        User.objects.create(name=name, surname=surname, username=username, email=email,
                            tel_number=tel_number, city=city, age=age, interests=interests,
                            password=make_password(password))
        return JsonResponse({'status': True, 'message': "Uspješno ste se registrovali."}, status=status.HTTP_201_CREATED)


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
        return JsonResponse({'status': False, 'message': "Lozinke se ne podudaraju"}, status=status.HTTP_400_BAD_REQUEST)
    elif len(owner) > 0:
        return JsonResponse({'status': False, 'message': "Email je već registrovan."}, status=status.HTTP_400_BAD_REQUEST)
    else:
        Owner.objects.create(name=name, surname=surname, username=username, email=email,
                             tel_number=tel_number, location=location, capacity=capacity, type=type_of_user,
                             password=make_password(password))
        return JsonResponse({'status': True, 'message': "Uspješno ste se registrovali."}, status=status.HTTP_401_UNAUTHORIZED)


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
        print("usao")
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
                                      "name": user.name, "surname": user.surname, "picture": user_picture}}
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
    if (User.objects.filter(email=email).exists() == False & Owner.objects.filter(email=email).exists() == False):
        return JsonResponse({'status': False, 'message': 'Korisnik sa unesenim emailom nije registrovan'}, status=status.HTTP_404_NOT_FOUND)
    else:
        if (User.objects.filter(email=email).exists() == True):
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
            return JsonResponse({'status': True, 'message': 'Nova lozinka Vam je poslana na '+email}, status=status.HTTP_200_OK)
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
            return JsonResponse({'status': True, 'message': 'Nova lozinka Vam je poslana na '+email}, status=status.HTTP_200_OK)


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

    if owner_id is not None:
        SportHall.objects.create(title=title, city=city, address=address,
                                 description=description, status=sport_hall_status, price=price, capacity=capacity, owner_id_id=owner_id)
        return Response({'data': {title, city, address, description,  price}, 'message': 'Uspješno kreiran novi teren.'}, status=status.HTTP_200_OK)
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
                'status': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Indicates if the request was successful'),
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
    array_of_sporthalls = []
    array_of_sporthalls.append(owner)
    array_of_sporthalls.append(sporthall)
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
