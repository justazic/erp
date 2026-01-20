from django.db import models
from students.models import Student
from accounts.models import User

# Create your models here.

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=[('present', 'Bor'), ('absent', 'Yoq')])
    marked_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)