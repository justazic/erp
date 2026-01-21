from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from accounts.models import User
from attendance.models import Attendance
from .models import Enrollment

class MyAttendanceView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.role != 'student':
            return redirect('/')
        attendance_records = Attendance.objects.filter(student=request.user).select_related('schedule__group', 'schedule__group__course')
        return render(request, 'students/my_attendance.html', {
            'attendance_records': attendance_records,
        })

class StudentListView(LoginRequiredMixin, View):
    def get(self, request):
        if not request.user.is_staff and request.user.role != 'teacher':
            return redirect('/')
        
        search = request.GET.get('search', '')
        students = User.objects.filter(role='student')
        
        if search:
            students = students.filter(
                Q(username__icontains=search) |
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(email__icontains=search)
            )
            
        return render(request, 'students/list.html', {
            'students': students,
            'search': search,
        })
