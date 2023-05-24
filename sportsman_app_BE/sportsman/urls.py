from django.urls import path, re_path
from . import views

urlpatterns = [
    path('authentication/login', views.login, name="login"),
    path('authentication/logout', views.logout, name='logout'),
    path('authentication/register-player',
         views.registration_player, name='registrationPlayer'),
    path('authentication/register-owner',
         views.registration_owner, name='registrationOwner'),
    path('filtered-sport-halls/', views.get_filtered_sport_halls, name='getFilteredSportHalls'),
    path('authentication/forgot-password',
         views.forgot_password, name='forgotPassword'),
    re_path(r'^authentication/confirm-email/$',
            views.confirm_email, name='confirm_email'),
    path('players', views.get_all_players, name='getAllUsers'),
    path('owners', views.get_all_owners, name='getAllOwners'),
    path('sport-halls', views.get_all_sport_halls, name='getAllSportHalls'),
    path('add-sport-hall', views.add_new_sport_hall, name='addNewSportHall'),
    path('get-sport-hall', views.get_sport_hall, name='getSportHall'),
    path('remove-sport-hall', views.remove_sport_hall, name='removeSportHall'),
    path('change-sport-hall-status',
         views.change_sporthall_status, name='changeSportHallStatus'),
    path('registration/player/',views.registrationPlayer,name='registrationPlayer'),
    path('registration/owner/',views.registrationOwner,name='registrationOwner'),
    path('player/<int:id>/', views.get_user_data, name="getUserData"),
    path('update/player/<int:id>/', views.update_user, name="updateUser"),
    path('login/',views.login,name='login')
]
