from django.urls import path

from . import views

urlpatterns = [
    path('registration/player/', views.registration_player, name='registrationPlayer'),
    path('registration/owner/', views.registration_owner, name='registrationOwner'),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name='logout'),
]
