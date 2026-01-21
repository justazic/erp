from django.db import models
from accounts.models import User
from students.models import Enrollment


class Payment(models.Model):
    PAYMENT_STATUS = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
        ('cancelled', 'Cancelled'),
    ]

    PAYMENT_TYPE = [
        ('tuition', 'Tuition Fee'),
        ('registration', 'Registration Fee'),
        ('exam', 'Exam Fee'),
        ('deposit', 'Deposit'),
        ('monthly', 'Monthly Charge'),
        ('other', 'Other'),
    ]

    PAYMENT_METHOD = [
        ('cash', 'Cash'),
        ('card', 'Card'),
        ('bank', 'Bank Transfer'),
        ('cheque', 'Cheque'),
        ('balance', 'Student Balance'),
    ]

    student = models.ForeignKey(User, on_delete=models.PROTECT, related_name='payments', limit_choices_to={
      'role': 'student',
      },
                                )
    enrollment = models.ForeignKey(Enrollment, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='payments',
                                   )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPE, default='tuition')
    method = models.CharField(max_length=20, choices=PAYMENT_METHOD)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    due_date = models.DateField()
    paid_date = models.DateField(null=True, blank=True)
    reference_number = models.CharField(max_length=100, unique=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student} - {self.amount} ({self.status})"

    class Meta:
        ordering = ['-due_date']
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'
