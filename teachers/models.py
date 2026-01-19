from django.db import models
from accounts.models import User
# Create your models here.


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    speciality = models.CharField(max_length=100)
    
    def __str__(self):
        return self.user.username
    
    