from django.db import models
from teachers.models import Teacher
from accounts.models import User


class Course(models.Model):
    name = models.CharField(max_length=100)
    small_image = models.ImageField(upload_to='courses/small_images', null=True)
    large_image = models.ImageField(upload_to='courses/large_images', null=True)
    small_description = models.TextField(max_length=50)
    large_description = models.TextField(max_length=1000)
    price = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'

    
class Group(models.Model):
    name = models.CharField(max_length=50)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ('name',)
        verbose_name = 'Group'
        verbose_name_plural = 'Groups'


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
