from django.db import models
from accounts.models import User
# Create your models here.


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    speciality = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True)
    bio = models.TextField(blank=True)
    experience_year = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.user.username
    
    