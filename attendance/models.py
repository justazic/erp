from django.core.exceptions import ValidationError
from django.db import models

from accounts.models import User
from courses.models import Group
from students.models import Enrollment


class Schedule(models.Model):
  DAY_CHOICES = [ (i,
                   d) for i, d in
                  enumerate([ 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday' ]) ]

  group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='schedule_slots')
  teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='schedule_slots',
                              limit_choices_to={
                                'role': 'teacher',
                                },
                              )
  day_of_week = models.IntegerField(choices=DAY_CHOICES)
  start_time = models.TimeField()
  end_time = models.TimeField()
  room = models.CharField(max_length=50, blank=True, null=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__( self ):
    return f"{self.group.name} - {self.get_day_of_week_display()} {self.start_time}"

  class Meta:
    ordering = ('day_of_week',
                'start_time')
    verbose_name = 'Schedule'
    verbose_name_plural = 'Schedules'
    unique_together = ('group',
                       'day_of_week',
                       'start_time')

  def clean( self ):
    if self.teacher:
      conflicts = Schedule.objects.filter(
        teacher=self.teacher,
        day_of_week=self.day_of_week,
        ).exclude(pk=self.pk)

      for s in conflicts:
        if not (self.end_time <= s.start_time or self.start_time >= s.end_time):
          raise ValidationError(f"Teacher conflict: {s.start_time} - {s.end_time}")

  def save( self, *args, **kwargs ):
    self.clean()
    super().save(*args, **kwargs)


class Attendance(models.Model):
  STATUS_CHOICES = [
    ('present',
     'Present'),
    ('absent',
     'Absent'),
    ('late',
     'Late'),
    ('excused',
     'Excused'),
    ]

  schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name='attendance_records', null=True,
                               blank=True,
                               )
  student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attendance_records', limit_choices_to={
    'role': 'student',
    },
                              )
  date = models.DateField()
  status = models.CharField(max_length=10, choices=STATUS_CHOICES)
  marked_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                related_name='marked_attendances', limit_choices_to={
      'role': 'teacher',
      },
                                )
  notes = models.TextField(blank=True, null=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__( self ):
    return f"{self.student} - {self.date} - {self.status}"

  class Meta:
    ordering = [ '-date' ]
    verbose_name = 'Attendance'
    verbose_name_plural = 'Attendances'
    unique_together = ('student',
                       'schedule',
                       'date')
    indexes = [
      models.Index(fields=[ 'student', 'date' ]),
      models.Index(fields=[ 'schedule', 'date' ]),
      ]
