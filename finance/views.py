from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Payment
from accounts.models import User
from django.db.models import Sum


# Create your views here.


class PaymentCreateView(LoginRequiredMixin, View):
    def get(self, request):
        students = Student.objects.all()
        return render(request, 'finance/payment_form.html', {
          'students': students,
          },
                      )
    
    
    def post(self, request):
        Payment.objects.create(
            student_id=request.POST.get('student'),
          amount=request.POST.get('amount'),
            method=request.POST.get('method')
        )
        return redirect('finance_report')


class FinanceReportView(LoginRequiredMixin, View):
    def get(self, request):
      payments = Payment.objects.all()
        total = payments.aggregate(Sum('amount'))['amount__sum'] or 0

      return render(request, 'finance/report.html', {
        'payments': payments,
        'total': total,
        },
                    )
