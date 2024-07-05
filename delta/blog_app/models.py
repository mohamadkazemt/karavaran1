from django.db import models


class User(models.Model):
    username = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    age = models.IntegerField()
   
    def __str__(self):
        return self.username