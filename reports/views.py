from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from students.models import Student
from finance.models import Payment
from django.db.models import Sum


# Create your views here.

class DashboardView(LoginRequiredMixin, View):
  def get( self, request ):
    total_students = Student.objects.count()
    total_income = Payment.objects.aggregate(Sum('amount'))[ 'amount__sum' ] or 0
    return render(request, 'dashboard.html', {
      'students': total_students,
      'income': total_income
      }
                  )
