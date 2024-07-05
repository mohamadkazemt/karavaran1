from django.db import models


class course(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    situation = models.BooleanField(default=True)
    views = models.IntegerField(default=0)
    
    def __str__(self):
        return f'{self.title}-{self.description[:5]}'
