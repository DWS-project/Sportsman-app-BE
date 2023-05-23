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
         views.forgot_password, name='forgotPassword'),
    path('players', views.get_all_players, name='getAllUsers'),
    path('owners', views.get_all_owners, name='getAllOwners'),
    path('sport-halls', views.get_all_sport_halls, name='getAllSportHalls'),
    path('player/<int:id>/', views.get_user_data, name="getUserData"),
    path('owner/<int:id>/', views.get_owner_data, name="getOwnerData"),
    path('update/player/<int:id>/', views.update_user, name="updateUser"),
    path('update_password/player/<int:id>/', views.update_user_password, name="updateUserPassword"),
    path('update_photo/player/<int:id>/', views.update_user_photo, name="updateUserPhoto"),
    path('update_owner/<int:id>/', views.update_owner, name="updateOwner"),
    path('update_password/owner/<int:id>/', views.update_owner_password, name="updateOwnerPassword"),
]
