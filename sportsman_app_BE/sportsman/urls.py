from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name='logout'),
    path('register-player/', views.registration_player, name='registrationPlayer'),
    path('register-owner/', views.registration_owner, name='registrationOwner'),
]
