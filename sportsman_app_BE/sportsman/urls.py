from django.urls import path
from . import views

urlpatterns = [
    path('authentication/login', views.login, name="login"),
    path('authentication/logout', views.logout, name='logout'),
    path('authentication/register-player',
         views.registration_player, name='registrationPlayer'),
    path('authentication/register-owner',
         views.registration_owner, name='registrationOwner'),
    path('authentication/forgot-password',
         views.forgotPassword, name='forgotPassword'),
    path('players', views.getAllPlayers, name='getAllUsers'),
    path('owners', views.getAllOwners, name='getAllOwners'),
]
