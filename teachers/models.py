from django.db import models

from accounts.models import User


class TeacherCourse(models.Model):
  teacher = models.ForeignKey(User, on_delete=models.CASCADE)
  course = models.ForeignKey('courses.Course', on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return f"{self.teacher} - {self.course}"

  class Meta:
    ordering = ['teacher', 'course']
