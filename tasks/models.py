from django.db import models
from accounts.models import User
from courses.models import Group
from django.utils import timezone


class Assignment(models.Model):
  STATUS_CHOICES = (
    ('draft',
     'Draft'),
    ('published',
     'Published'),
    ('closed',
     'Closed'),
    )

  teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assignments', limit_choices_to={
    'role': 'teacher',
    },
                              )
  group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='assignments', null=True, blank=True)
  title = models.CharField(max_length=100)
  description = models.TextField()
  status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='draft')
  deadline = models.DateTimeField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__( self ):
    return self.title

  class Meta:
    ordering = ('-created_at',)
    verbose_name = 'Assignment'
    verbose_name_plural = 'Assignments'

  def is_expired( self ):
    return timezone.now() > self.deadline

  def get_submission_count( self ):
    return self.submissions.count()


class Submission(models.Model):
  STATUS_CHOICES = (
    ('submitted',
     'Submitted'),
    ('graded',
     'Graded'),
    ('late',
     'Late'),
    )

  assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
  student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submissions', limit_choices_to={
    'role': 'student',
    },
                              )
  file = models.FileField(upload_to='submissions/%Y/%m/%d/')
  comment = models.TextField(blank=True)
  grade = models.IntegerField(blank=True, null=True)
  status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='submitted')
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__( self ):
    return f"{self.student} - {self.assignment}"

  class Meta:
    ordering = ('-created_at',)
    verbose_name = 'Submission'
    verbose_name_plural = 'Submissions'
    unique_together = ('assignment',
                       'student')
