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
    path('add-sport-hall', views.add_new_sport_hall, name='addNewSportHall'),
    path('get-sport-hall', views.get_sport_hall, name='getSportHall'),
    path('remove-sport-hall', views.remove_sport_hall, name='removeSportHall'),
    path('change-sport-hall-status',
         views.change_sporthall_status, name='changeSportHallStatus'),
    path('createTeam/', views.create_team, name='createTeam'),
    path('getTeams/', views.get_perm_teams, name='getTeams'),
    path('deleteTeam/', views.delete_team, name='deleteTeam'),
    path('inviteTeamMember/', views.invite_team_member, name='inviteTeamMember'),
    path('deleteTeamMember/', views.delete_team_member, name='deleteTeamMember'),

]
