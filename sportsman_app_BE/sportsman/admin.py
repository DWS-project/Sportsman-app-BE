from django.contrib import admin

# Register your models here.
from .models import UserType
from .models import User

admin.site.register(UserType)
admin.site.register(User)