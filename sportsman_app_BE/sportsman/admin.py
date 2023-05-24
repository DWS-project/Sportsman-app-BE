from django.contrib import admin

# Register your models here.
from .models import UserType, Friends, Invitations, Team, TeamMembers, PermanentTeams, SportHall, Games, Owner
from .models import User

admin.site.register(UserType)
admin.site.register(User)
admin.site.register(Friends)
admin.site.register(Invitations)
admin.site.register(Team)
admin.site.register(TeamMembers)
admin.site.register(PermanentTeams)
admin.site.register(SportHall)
admin.site.register(Games)
admin.site.register(Owner)