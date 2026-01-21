from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE = (
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    )
    
    role = models.CharField(max_length=10, choices=ROLE)
    avatar = models.ImageField(upload_to='avatar/', default='')
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=250, blank=True, null=True)

    speciality = models.CharField(max_length=100, blank=True, null=True)
    qualifications = models.TextField(blank=True, null=True)
    is_expert = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username

    class Meta:
        ordering = ['-id']
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def save( self, *args, **kwargs ):
        if self.role == 'admin':
            self.is_staff = True
            self.is_superuser = True
        super().save(*args, **kwargs)

