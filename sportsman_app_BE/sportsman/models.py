from django.db import models

# Create your models here.
class UserType(models.Model):
    name=models.CharField(max_length=20)
    def __str__(self):
        return self.name

class User(models.Model):
    username=models.CharField(max_length=50)
    name=models.CharField(max_length=50)
    surname=models.CharField(max_length=50)
    email=models.EmailField(max_length=50)
    password=models.CharField(max_length=20)
    typeOfUser=models.ForeignKey(UserType,null=True,on_delete=models.SET_NULL)

    def __str__(self):
        return self.email