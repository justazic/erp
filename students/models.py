from django.db import models

from courses.models import Course, Session


class Enrollment(models.Model):
  STATUS_CHOICES = (('graduated', 'Graduated'), ('failed', 'Failed'), ('studying', 'Studying'), ('dropped', 'Dropped'),)

  student = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='enrollments', limit_choices_to={
    'role': 'student',
    }, )
  course = models.ForeignKey(Course, related_name='enrollments', on_delete=models.CASCADE)
  session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='enrollments', null=True, blank=True)
  group = models.ForeignKey('courses.Group', on_delete=models.SET_NULL, related_name='enrollments', null=True, blank=True)
  status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='studying')
  grade = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
  last_attended = models.DateField(null=True, blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__( self ):
    return f"{self.student.username} - {self.course.name}"

  class Meta:
    ordering = [ '-created_at' ]
    verbose_name = 'Enrollment'
    verbose_name_plural = 'Enrollments'
    unique_together = ('student', 'course')
