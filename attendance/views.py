from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Attendance
from students.models import Student
from datetime import date

# Create your views here.


class AttendanceCreateView(LoginRequiredMixin,View):
    def get(self, request):
        students = Student.objects.all()
        return render(request, 'attendance/form.html', {'students':students})
    
    def post(self, requdet):
        Attendance.objects.create(
            student_id = requdet.POST.get('student'),
            date=date.today(),
            status=requdet.POST.get('status')
        )
        return redirect('/')