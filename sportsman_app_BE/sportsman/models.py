from django.db import models


# Create your models here.
class UserType(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class User(models.Model):
    username = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=20)
    city = models.CharField(max_length=50, null=True)
    tel_number = models.CharField(max_length=20, null=True)
    age = models.IntegerField(null=True)
    interests = models.TextField(null=True)
    picture = models.CharField(max_length=50, null=True)
    ROLE_CHOICES = (
        ('renter', 'Renter'),
        ('owner', 'Owner'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='owner')
    access_token = models.TextField(null=True)

    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def is_user(self):
        return self.role == 'user'


def __str__(self):
    return self.email


class Friends(models.Model):
    user1 = models.ForeignKey(User, related_name='friends1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, related_name='friends2', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user1) + " " + str(self.user2)


class Invitations(models.Model):
    time_sent = models.DateTimeField(null=True)
    sender = models.ForeignKey(User, related_name='sent_invitations', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='received_invitations', on_delete=models.CASCADE)
    status = models.IntegerField()
    details = models.TextField(null=True)

    def __str__(self):
        return "sender: " + str(self.sender) + " recipient:" + str(self.recipient) + "status"


class Team(models.Model):
    team_lead_id = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.team_lead_id


class TeamMembers(models.Model):
    team_id = models.ForeignKey(Team, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.team_id) + " " + str(self.user_id)


class PermanentTeams(models.Model):
    team_id = models.ForeignKey(Team, on_delete=models.CASCADE)

    def __str__(self):
        return self.team_id


class Owner(models.Model):
    username = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=20)
    location = models.TextField(null=True)
    tel_number = models.CharField(max_length=20, null=True)
    capacity = models.IntegerField(null=True)
    type = models.CharField(max_length=10, null=True)
    picture = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.email


class SportHall(models.Model):
    title = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    address = models.TextField(null=True)
    sports = models.TextField(null=True)
    description = models.CharField(max_length=500, null=True)
    owner_id = models.ForeignKey(Owner, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, null=True)
    price = models.FloatField()
    type = models.CharField(max_length=20, null=True)
    pictures = models.TextField(null=True)

    def __str__(self):
        return "title: " + str(self.title) + " owner: " + str(self.owner_id)


class Games(models.Model):
    hall_name = models.CharField(max_length=50)
    team_id = models.ForeignKey(Team, on_delete=models.CASCADE)
    status = models.IntegerField()
    time_appointed = models.DateTimeField(null=True)

    def __str__(self):
        return "hall: " + str(self.hall_name) + " Team_id: " + str(self.team_id) + "status: " + str(self.status)
