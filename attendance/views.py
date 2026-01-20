from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Attendance
from students.models import Student

# Create your views here.


class AttendanceCreateView(LoginRequiredMixin,View):
    def get(self, request):
        students = Student.objects.select_related('user')
        return render(request, 'attendance/form.html', {'students':students})
    
    def post(self, request):
        Attendance.objects.create(
            student_id = request.POST.get('student'),
            status=request.POST.get('status')
        )
        return redirect('/')