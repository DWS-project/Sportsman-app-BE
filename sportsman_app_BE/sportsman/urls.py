from django.urls import path, re_path
from . import views

urlpatterns = [
    path('authentication/login', views.login, name="login"),
    path('authentication/logout', views.logout, name='logout'),
    path('authentication/register-player',
         views.registration_player, name='registrationPlayer'),
    path('authentication/register-owner',
         views.registration_owner, name='registrationOwner'),
    path('filtered-sport-halls/', views.get_filtered_sport_halls,
         name='getFilteredSportHalls'),
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
<<<<<<< HEAD
    path('createTeam/', views.create_team, name='createTeam'),
    path('getTeams/', views.get_perm_teams, name='getTeams'),
    path('deleteTeam/', views.delete_team, name='deleteTeam'),
    path('inviteTeamMember/', views.invite_team_member, name='inviteTeamMember'),
    path('deleteTeamMember/', views.delete_team_member, name='deleteTeamMember'),

=======
    path('contact-us', views.contact_us, name='contactUs'),
    path('player/<int:id>', views.get_player_data, name="getPlayerData"),
    path('owner/<int:id>', views.get_owner_data, name="getOwnerData"),
    path('player/update/<int:id>', views.update_player_data, name="updatePlayerData"),
    path('player/change-password/<int:id>', views.update_player_password, name="updateUserPassword"),
    path('player/change-profile-photo/<int:id>', views.update_player_photo, name="updateUserPhoto"),
    path('owner/update/<int:id>', views.update_owner_data, name="updateOwner"),
    path('owner/change-password/<int:id>', views.update_owner_password, name="updateOwnerPassword"),
>>>>>>> 0c5628bad9ce2a212e921c7d94e644839115f25d
]
