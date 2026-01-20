from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from .models import Payment
from students.models import Student


class PaymentCreateView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.role != 'admin':
            return redirect('/')

        students = Student.objects.all()
        return render(
            request,
            'finance/payment_form.html',
            {'students': students}
        )

    def post(self, request):
        if request.user.role != 'admin':
            return redirect('/')

        Payment.objects.create(
            student_id=request.POST.get('student'),
            amount=request.POST.get('amount'),
            method=request.POST.get('method')
        )
        return redirect('/finance/report/')


class FinanceReportView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.role != 'admin':
            return redirect('/')

        payments = Payment.objects.select_related('student', 'student__user')
        total = payments.aggregate(Sum('amount'))['amount__sum'] or 0

        return render(request,'finance/report.html',{'payments': payments,'total': total})
