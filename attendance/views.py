from datetime import date

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View

from students.models import Student
from .models import Attendance


class AttendanceCreateView(LoginRequiredMixin, View):
  def get( self, request ):
    if request.user.role not in [ 'admin', 'teacher' ]:
      return redirect('/')

    students = Student.objects.all()
    return render(request, 'attendance/form.html', {
      'students': students,
      }, )

  def post( self, request ):
    if request.user.role not in [ 'admin', 'teacher' ]:
      return redirect('/')

    Attendance.objects.create(student_id=request.POST.get('student'), date=date.today(),
                              status=request.POST.get('status'), )
    return redirect('/')


class AttendanceListView(LoginRequiredMixin, View):
  def get( self, request ):
    if request.user.role not in [ 'admin', 'teacher' ]:
      return redirect('/')
