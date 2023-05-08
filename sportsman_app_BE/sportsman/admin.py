from django.contrib import admin

# Register your models here.
from .models import UserType, Friends, Invitations, Team, Team_members, Permanent_teams, Sport_hall, Games, Owner
from .models import User

admin.site.register(UserType)
admin.site.register(User)
admin.site.register(Friends)
admin.site.register(Invitations)
admin.site.register(Team)
admin.site.register(Team_members)
admin.site.register(Permanent_teams)
admin.site.register(Sport_hall)
admin.site.register(Games)
admin.site.register(Owner)