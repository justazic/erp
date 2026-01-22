from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.db.models import Q
from django.http import JsonResponse
from datetime import timedelta
from .models import Schedule, Attendance
from students.models import Enrollment
from tasks.models import Assignment
from django.core.exceptions import PermissionDenied
from tasks.models import Submission
from accounts.models import User
import json


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


class ScheduleDetailView(LoginRequiredMixin, DetailView):
  model = Schedule
  template_name = 'attendance/schedule_detail.html'
  context_object_name = 'schedule'
  pk_url_kwarg = 'schedule_id'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    schedule = self.object
    today = timezone.now().date()

    # Calculate the date for this schedule's day_of_week
    current_day_of_week = today.weekday()  # Monday=0, Sunday=6
    target_day_of_week = schedule.day_of_week

    # Calculate days difference
    days_diff = (target_day_of_week - current_day_of_week) % 7
    if days_diff == 0:
      # Use today if it's the same day of week
      attendance_date = today
    else:
      # Find the most recent past occurrence
      if days_diff <= current_day_of_week:
        attendance_date = today - timedelta(days=current_day_of_week - target_day_of_week)
      else:
        attendance_date = today - timedelta(days=(7 - days_diff))

    # Get all enrollments for this group
    enrollments = Enrollment.objects.filter(
      group=schedule.group,
      status='studying',
    ).select_related('student')

    # Get attendance records for this schedule's date
    attendance_records = Attendance.objects.filter(
      schedule=schedule,
      date=attendance_date,
    )
    attendance_map = {a.student_id: a for a in attendance_records}

    # Get assignments for this SPECIFIC schedule (lesson)
    assignments = Assignment.objects.filter(
      schedule=schedule,
      status='published',
    ).prefetch_related('submissions')

    # Build student data with attendance and assignment info
    students_data = []
    for enrollment in enrollments:
      student = enrollment.student
      attendance = attendance_map.get(student.id)

      # Get submission status for this student across all assignments for this schedule
      submissions = {}
      submission_list = []

      # Always process all assignments, even if no submissions
      for assignment in assignments:
        submission = next(
          (s for s in assignment.submissions.all() if s.student_id == student.id),
          None
        )
        submissions[assignment.id] = submission

        # Build submission data for display
        if submission:
          submission_list.append({
            'id': submission.id,
            'assignment_title': assignment.title,
            'status': submission.status,
            'grade': submission.grade,
          })
        else:
          # Add empty entry for assignments without submission
          submission_list.append({
            'id': None,
            'assignment_title': assignment.title,
            'status': 'not_submitted',
            'grade': None,
          })

      students_data.append({
        'enrollment': enrollment,
        'student': student,
        'attendance': attendance,
        'submissions': submissions,
        'submission_list': submission_list,
      })

    # Serialize students data to JSON for JavaScript (for modal functionality if needed)
    students_data_json = json.dumps([
      {
        'student_id': item['student'].id,
        'submissions': item['submission_list'],
      }
      for item in students_data
    ])

    context['students_data'] = students_data
    context['assignments'] = assignments
    context['today'] = today
    context['students_data_json'] = students_data_json

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


class MarkStudentAttendanceView(LoginRequiredMixin, View):
  """Mark attendance for a specific student on a specific schedule"""
  def post(self, request, schedule_id, student_id):
    schedule = get_object_or_404(Schedule, pk=schedule_id)
    student = get_object_or_404(User, pk=student_id, role='student')

    # Allow teacher of the group or admin
    if request.user.role not in ['teacher', 'admin']:
      return JsonResponse({'error': 'Permission denied'}, status=403)

    if request.user.role == 'teacher' and schedule.teacher != request.user:
      return JsonResponse({'error': 'Permission denied'}, status=403)

    # Calculate the date for this schedule's day_of_week
    # Find the most recent occurrence of this day of week (or today if it matches)
    today = timezone.now().date()
    current_day_of_week = today.weekday()  # Monday=0, Sunday=6
    target_day_of_week = schedule.day_of_week

    # Calculate days difference
    days_diff = (target_day_of_week - current_day_of_week) % 7
    if days_diff == 0:
      # Use today if it's the same day of week
      attendance_date = today
    else:
      # Find the most recent past occurrence
      if days_diff <= current_day_of_week:
        attendance_date = today - timedelta(days=current_day_of_week - target_day_of_week)
      else:
        attendance_date = today - timedelta(days=(7 - days_diff))

    status = request.POST.get('status')

    if status:
      Attendance.objects.update_or_create(
        schedule=schedule,
        student=student,
        date=attendance_date,
        defaults={
          'status': status,
          'marked_by': request.user,
          'notes': request.POST.get('notes', ''),
        }
      )
      return JsonResponse({'success': True})

    return JsonResponse({'error': 'No status provided'}, status=400)


class StudentSubmissionDetailView(LoginRequiredMixin, DetailView):
  """View and grade a student's submission"""
  model = Submission
  template_name = 'attendance/submission_detail.html'
  context_object_name = 'submission'
  pk_url_kwarg = 'submission_id'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    submission = self.object

    # Allow students to view their own submissions, or teachers to view submissions from their group
    if self.request.user.role == 'student':
      if submission.student != self.request.user:
        raise PermissionDenied()
    elif self.request.user.role == 'teacher':
      if submission.assignment.group.teacher != self.request.user:
        raise PermissionDenied()
    elif self.request.user.role != 'admin':
      raise PermissionDenied()

    context['assignment'] = submission.assignment
    context['student'] = submission.student

    return context

  def post(self, request, submission_id):
    submission = get_object_or_404(Submission, pk=submission_id)

    # Check permissions - allow teachers of the group or admins
    if request.user.role == 'teacher':
      if submission.assignment.group.teacher != request.user:
        raise PermissionDenied()
    elif request.user.role != 'admin':
      raise PermissionDenied()

    # Update submission with grade and feedback
    submission.grade = request.POST.get('grade')
    submission.comment = request.POST.get('comment', '')

    # Auto-determine status based on grade
    if submission.grade:
      submission.status = 'graded'
    elif submission.status == 'late':
      submission.status = 'late'
    else:
      submission.status = 'submitted'

    submission.save()

    # Redirect back to schedule detail
    return redirect('attendance:schedule_detail', schedule_id=submission.assignment.schedule.id)

