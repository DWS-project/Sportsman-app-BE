from django.urls import path

from . import views

urlpatterns = [
    path('registration/user/',views.registrationUser,name='registrationUser'),
    path('registration/owner/',views.registrationOwner,name='registrationOwner'),
    path('login/',views.login,name='login')
]
