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
    interests = models.CharField(max_length=500, null=True)
    picture = models.CharField(max_length=500, null=True)
    access_token = models.TextField(null=True)
    confirmation_token = models.TextField(null=True)
    last_login = models.DateTimeField(null=True)
    email_confirmed = models.BooleanField(default=False)
    user_type = models.ForeignKey(UserType, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.email


class Friends(models.Model):
    user1 = models.ForeignKey(
        User, related_name='friends1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(
        User, related_name='friends2', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user1) + " " + str(self.user2)


class InvitationType(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Invitations(models.Model):
    time_sent = models.DateTimeField(null=True)
    sender = models.ForeignKey(
        User, related_name='sent_invitations', on_delete=models.CASCADE)
    recipient = models.ForeignKey(
        User, related_name='received_invitations', on_delete=models.CASCADE)
    status = models.IntegerField()
    details = models.TextField(null=True)
    invitation_type = models.ForeignKey(InvitationType, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return "sender: " + str(self.sender) + " recipient: " + str(self.recipient) + \
            " status: " + str(self.status) + " time_sent: " + str(self.time_sent)


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
    team_name = models.CharField(max_length=30, null=True)

    def __str__(self):
        return str(self.team_id) + " " + str(self.team_name)


class Owner(User):
    location = models.TextField(null=True)
    capacity = models.IntegerField(null=True)

    def __str__(self):
        return self.email


class Sport(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class SportHall(models.Model):
    title = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    address = models.TextField(null=True)
    description = models.TextField(max_length=5000, null=True)
    status = models.CharField(max_length=20, null=True)
    price = models.FloatField()
    sports = models.ManyToManyField(Sport)
    type = models.CharField(max_length=20, null=True)
    pictures = models.TextField(null=True)
    capacity = models.IntegerField(null=True)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)

    def __str__(self):
        return "title: " + str(self.title)


class Owner_SportHall(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    sport_hall = models.ForeignKey(SportHall, on_delete=models.CASCADE)


class Status(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Games(models.Model):
    team_id = models.ForeignKey(Team, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    time_appointed = models.DateTimeField(null=True)
    sport_hall = models.ForeignKey(SportHall, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return "hall: " + str(self.sport_hall) + " Team_id: " + str(self.team_id) + "status: " + str(self.status)


class Reservations(models.Model):
    sport_hall_id = models.ForeignKey(SportHall, on_delete=models.CASCADE)
    user_id = models.IntegerField(null=True)
    date = models.DateField(null=True)
    time_from = models.TimeField(null=True)
    time_to = models.TimeField(null=True)
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    tel_number = models.CharField(max_length=20)
    team_id = models.IntegerField(null=True)

    def __str__(self):
        return "TimeBegin: " + str(self.time_from) + " TimeEnd: " + \
            str(self.time_to) + " email: " + str(self.email) + \
            " id: " + str(self.user_id)
