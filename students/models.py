from django.db import models
from accounts.models import User

# Create your models here.

class Student(models.Model):
    Status = (
        ('graduated', 'Graduated'),
        ('failed', 'Failed'),
        ('studying', 'Studying'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=250)
    status = models.CharField(max_length=10, choices=Status)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('user__username',)
        verbose_name = 'Student'
        verbose_name_plural = 'Students'

    def __str__(self):
        return self.user.username

