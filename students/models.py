from django.db import models
from accounts.models import User

# Create your models here.

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phonde = models.CharField(max_length=20)
    address = models.CharField(max_length=250)
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.user.username