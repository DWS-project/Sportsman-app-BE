from django.urls import path, re_path
from . import views

urlpatterns = [
    path('authentication/login', views.login, name="login"),
    path('authentication/logout', views.logout, name='logout'),
    path('authentication/register-player',
         views.registration_player, name='registrationPlayer'),
    path('authentication/register-owner',
         views.registration_owner, name='registrationOwner'),
    path('authentication/change-password/<int:id>', views.update_user_password, name="updateUserPassword"),
    re_path(r'^authentication/confirm-email/$',
            views.confirm_email, name='confirm_email'),
    path('get-sport-hall-user', views.get_sport_hall_user, name='getSportHallUser'),
    path('get-sport-hall-reservations', views.get_sport_hall_reservations, name='getSportHallReservations'),
    path('get-friends', views.get_friends, name='getFriends'),
    path('reservation', views.reservation, name='reservation'),
    path('get-permanent-teams', views.get_permanent_teams, name='getPermanentTeams'),
    path('get-users', views.get_users, name='getUsers'),
    path('get-invited-users', views.get_invited_users, name='getInvitedUsers'),
    path('invite-temporary-team', views.invite_temporary_team, name='inviteTemporaryTeam'),
    path('remove-invite-temporary-team',
         views.remove_invite_temporary_team, name='removeInviteTemporaryTeam'),
    path('authentication/resend-confirmation-email',
         views.resend_confirmation_email, name='resendConfirmationEmail'),
    path('authentication/forgot-password',
         views.forgot_password, name='forgotPassword'),

    path('owner/all', views.get_all_owners, name='getAllOwners'),
    path('owner/<int:id>', views.get_owner_data, name="getOwnerData"),
    path('owner/update/<int:id>', views.update_owner_data, name="updateOwner"),

    path('sport-hall', views.get_all_sport_halls, name='getAllSportHalls'),
    path('sport-hall/<int:owner_id>/<int:sporthall_id>', views.get_sport_hall, name='getSportHall'),
    path('sport-hall', views.add_new_sport_hall, name='addNewSportHall'),
    path('sport-hall/remove', views.remove_sport_hall, name='removeSportHall'),
    path('sport-hall/change-status',
         views.change_sport_hall_status, name='changeSportHallStatus'),

    path('team/all', views.get_perm_teams, name='getTeams'),
    path('team/', views.create_team, name='createTeam'),
    path('team/delete/', views.delete_team, name='deleteTeam'),
    path('team/invite-member/', views.invite_team_member, name='inviteTeamMember'),
    path('team/delete-member/', views.delete_team_member, name='deleteTeamMember'),

    path('player/all', views.get_all_players, name='getAllUsers'),
    path('player/<int:id>', views.get_player_data, name="getPlayerData"),
    path('player/update', views.update_player_data, name="updatePlayerData"),
    path('player/change-profile-photo/<int:id>/', views.update_player_photo, name="updateUserPhoto"),

    path('contact-us', views.contact_us, name='contactUs'),

    path('player/invitation/<int:id>/', views.get_player_invitations, name="getPlayerInvitations"),
    path('player/invitation/status/<int:invitation_id>/', views.update_invitation_status, name="updateInvitationStatus"),

    path('player/friends/<int:id>', views.get_player_friends, name="getPlayerFriends"),
    path('player/friends/sort-history/<int:id>', views.sort_player_history, name="sortPlayerHistory"),
    path('player/friends/sort-friends/<int:player_id>', views.sort_player_friends, name="sortPlayerFriends"),

    path('player/games/<int:user_id>', views.get_player_games, name="getPlayerGames"),
]
