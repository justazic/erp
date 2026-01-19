from django.db import models
from teachers.models import Teacher

# Create your models here.

class Course(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
    
class Group(models.Model):
    name = models.CharField(max_length=50)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return self.name
    
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=-models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    