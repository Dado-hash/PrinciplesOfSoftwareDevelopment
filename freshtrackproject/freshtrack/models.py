from django.db import models


class User(models.Model):
    firstname = models.CharField(max_length=100)  # Specify the max_length attribute
    lastname = models.CharField(max_length=100)  # Specify the max_length attribute
    email = models.EmailField()
    password = models.CharField(max_length=100)   # Specify the max_length attribute
    age = models.IntegerField()

    def __str__(self):
        return self.firstname + ' ' + self.lastname
    