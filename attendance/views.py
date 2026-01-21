from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.db.models import Q
from .models import Schedule, Attendance
from students.models import Enrollment


class ScheduleListView(LoginRequiredMixin, ListView):
  model = Schedule
  template_name = 'attendance/schedule_list.html'
  context_object_name = 'schedules'
  paginate_by = 20

  def get_queryset( self ):
    search = self.request.GET.get('search', '')
    qs = Schedule.objects.select_related('group', 'teacher')
    
    if self.request.user.role == 'teacher':
        qs = qs.filter(teacher=self.request.user)
    
    if search:
        qs = qs.filter(
            Q(group__name__icontains=search) |
            Q(group__course__name__icontains=search) |
            Q(room__icontains=search)
        )
    return qs

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['search'] = self.request.GET.get('search', '')
    return context


class MarkAttendanceView(LoginRequiredMixin, View):
  def get( self, request, schedule_id ):
    schedule = get_object_or_404(Schedule, pk=schedule_id)

    if request.user.role != 'teacher' or schedule.teacher != request.user:
      return redirect('attendance:schedule_list')

    today = timezone.now().date()
    enrollments = Enrollment.objects.filter(
      group=schedule.group,
      status='studying',
      )

    attendance_today = Attendance.objects.filter(
      schedule=schedule,
      date=today,
      )

    context = {
      'schedule': schedule,
      'date': today,
      'enrollments': enrollments,
      'attendance_records': { a.student_id: a for a in attendance_today },
      }

    return render(request, 'attendance/mark_attendance.html', context)

  def post( self, request, schedule_id ):
    schedule = get_object_or_404(Schedule, pk=schedule_id)

    if request.user.role != 'teacher' or schedule.teacher != request.user:
      return redirect('attendance:schedule_list')

    today = timezone.now().date()
    enrollments = Enrollment.objects.filter(
      group=schedule.group,
      status='studying',
      )

    for enrollment in enrollments:
      student = enrollment.student
      status = request.POST.get(f'status_{student.id}')

      if status:
        Attendance.objects.update_or_create(
          schedule=schedule,
          student=student,
          date=today,
          defaults={
            'status': status,
            'marked_by': request.user,
            'notes': request.POST.get(f'notes_{student.id}', ''),
            },
          )

    return redirect('attendance:schedule_list')
