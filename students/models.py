from django.db import models
from accounts.models import User
from courses.models import Group

# Create your models here.

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=250)
    birth_date = models.DateField(blank=True, null=True)
    joined_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.user.username