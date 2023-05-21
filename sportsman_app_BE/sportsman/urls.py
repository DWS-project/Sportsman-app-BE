from django.urls import path
from . import views

urlpatterns = [
    path('authentication/login/', views.login, name="login"),
    path('authentication/logout/', views.logout, name='logout'),
    path('authentication/register-player/',
         views.registration_player, name='registrationPlayer'),
    path('authentication/register-owner/',
         views.registration_owner, name='registrationOwner'),
    path('landing-page-cards/', views.landing_page, name='landingPage'),
]
