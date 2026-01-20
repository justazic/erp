from django.db import models
from students.models import Student


class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=[('present', 'Bor'), ('absent', 'Yoq')])

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student} - {self.date} - {self.status}"

    class Meta:
        ordering = ['-date']
        verbose_name = 'Attendance'
        verbose_name_plural = 'Attendances'
        unique_together = ('student', 'date')



