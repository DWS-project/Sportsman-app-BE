from django.urls import path

from . import views

urlpatterns = [
    path('registration/player/',views.registrationPlayer,name='registrationPlayer'),
    path('registration/owner/',views.registrationOwner,name='registrationOwner'),
    path('player/<int:id>/', views.get_user_data, name="getUserData"),
    path('update/player/<int:id>/', views.update_user, name="updateUser"),
    path('login/',views.login,name='login')
]
