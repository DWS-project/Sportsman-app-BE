from django.urls import path

from . import views

urlpatterns = [
    path('registration/player/',views.registrationPlayer,name='registrationPlayer'),
    path('registration/owner/',views.registrationOwner,name='registrationOwner'),
    path('login/',views.login,name='login')
]
