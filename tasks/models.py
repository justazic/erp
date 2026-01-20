from django.db import models
from teachers.models import Teacher
from students.models import Student
from django.utils import timezone


class Assignment(models.Model):
  teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
  title = models.CharField(max_length=100)
  description = models.TextField(max_length=200)
  deadline = models.DateTimeField()
  created_at = models.DateField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.title

  class Meta:
    ordering = ('-created_at',)
    verbose_name = 'Assignment'
    verbose_name_plural = 'Assignments'


  def is_expired( self ):
    return timezone.now() > self.deadline


class Submission(models.Model):
  assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
  student = models.ForeignKey(Student, on_delete=models.CASCADE)
  file = models.FileField(upload_to='submission/')
  comment = models.TextField(blank=True)
  grade = models.IntegerField(blank=True, null=True)
  checked = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return f"{self.student} - {self.assignment}"

  class Meta:
    ordering = ('-created_at',)
