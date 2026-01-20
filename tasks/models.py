from django.db import models
from teachers.models import Teacher
from students.models import Student
from django.utils import timezone

# Create your models here.

class Assignment(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=200)
    deadline = models.DateTimeField()
    created_at = models.DateField(auto_now_add=True)
    
    def is_expired(self):
        return timezone.now() > self.deadline
    
class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    file = models.FileField(upload_to='submission/')
    comment = models.TextField(blank=True)
    grade = models.IntegerField(blank=True, null=True)
    checked = models.BooleanField(default=False)
    
    