from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import TemplateView

from django.db.models import Count, Q
from courses.models import Group, Session, Course, Category
from students.models import Enrollment
from tasks.models import Assignment, Submission
from finance.models import Payment
from attendance.models import Attendance, Schedule
from accounts.models import User

from .forms import LoginForm, UserProfileForm


class LoginView(View):
  def get( self, request ):
    if request.user.is_authenticated:
      return redirect('/')

    form = LoginForm()
    return render(request, 'auth/login.html', {
      'form': form,
      }, )

  def post( self, request ):
    form = LoginForm(request.POST)

    if not form.is_valid():
      return render(request, 'auth/login.html', {
        'form': form,
        'error': 'Please fill in all fields correctly.',
        }, )

    username = form.cleaned_data[ 'username' ]
    password = form.cleaned_data[ 'password' ]

    user = authenticate(request, username=username, password=password)

    if user is None:
      return render(request, 'auth/login.html', {
        'form': form,
        'error': 'Invalid username or password',
        }, )

    if not user.is_active:
      return render(request, 'auth/login.html', {
        'form': form,
        'error': 'Your account is disabled',
        }, )

    login(request, user)
    if user.role == 'teacher':
      return redirect('accounts:dashboard')
    if user.role == 'student':
      return redirect('accounts:dashboard')
    if user.role == 'admin':
      return redirect('courses:admin_dashboard')
    return redirect('/admin/')


class LogoutView(View):
  def get( self, request ):
    logout(request)
    return redirect('/accounts/login/')


@login_required
def profile( request ):
  user = request.user

  # default forms
  profile_form = UserProfileForm(request.POST or None, request.FILES or None, instance=user, user=user, )
  password_form = PasswordChangeForm(user)

  # ---------- PROFILE UPDATE ----------
  if request.method == "POST" and "update_profile" in request.POST:
    if profile_form.is_valid():
      profile_form.save()
      messages.success(request, "Profile updated successfully.")
      return redirect("accounts:profile")
    else:
      messages.error(request, "Please fix the errors in your profile form.")

  # ---------- PASSWORD CHANGE ----------
  if request.method == "POST" and "change_password" in request.POST:
    password_form = PasswordChangeForm(user, request.POST)
    if password_form.is_valid():
      password_form.save()
      update_session_auth_hash(request, password_form.user)  # keep user logged in
      messages.success(request, "Password changed successfully.")
      return redirect("accounts:profile")
    else:
      # keep modal open on errors (template JS checks this flag)
      messages.error(request, "Please fix the password errors.")

  # ---------- DELETE ACCOUNT (2-step confirm) ----------
  if request.method == "POST" and "delete_account" in request.POST:
    step = request.POST.get("delete_step", "1")
    if step == "2":
      # final confirm -> delete
      user.delete()
      messages.success(request, "Your account has been deleted.")
      return redirect("index")
    else:
      # step 1 handled by modal UI; we don't delete here
      messages.error(request, "Please confirm deletion again.")

  ctx = {
    "profile_user": user,
    "profile_form": profile_form,
    "password_form": password_form,
    "open_password_modal": bool(password_form.errors),
    "open_edit_mode": bool(profile_form.errors),  # ✅ ADD THIS
    }
  return render(request, "accounts/profile.html", ctx)


class DashboardView(LoginRequiredMixin, TemplateView):
  def get_template_names( self ):
    user = self.request.user
    if user.role == 'teacher':
      return [ "dashboards/teacher.html" ]
    if user.role == 'student':
      return [ "dashboards/student.html" ]
    if user.role == 'admin':
      return [ "courses/admin/dashboard.html" ]
    return [ "dashboard.html" ]

  def get_context_data( self, **kwargs ):
    ctx = super().get_context_data(**kwargs)
    user = self.request.user
    
    if user.role == 'teacher':
        my_groups = Group.objects.filter(teacher=user).select_related('course', 'session')
        my_groups_count = my_groups.count()
        total_students_count = Enrollment.objects.filter(course__groups__in=my_groups).distinct().count()
        
        # Recent submissions for teacher's assignments
        pending_submissions = Submission.objects.filter(
            assignment__teacher=user, 
            status='submitted'
        ).select_related('student', 'assignment').order_by('-created_at')[:5]
        
        pending_reviews_count = Submission.objects.filter(assignment__teacher=user, status='submitted').count()
        
        ctx.update({
            "my_groups": my_groups,
            "my_groups_count": my_groups_count,
            "total_students_count": total_students_count,
            "pending_reviews_count": pending_reviews_count,
            "pending_submissions": pending_submissions,
        })
    elif user.role == 'student':
        enrollments = Enrollment.objects.filter(student=user).select_related('course', 'session', 'group')
        enrolled_groups_count = enrollments.filter(group__isnull=False).values('group').distinct().count()

        # Pending tasks: assignments for groups student is in, where no submission exists
        student_groups = Group.objects.filter(enrollments__student=user)
        pending_assignments = Assignment.objects.filter(
            group__in=student_groups,
            status='published'
        ).exclude(submissions__student=user).order_by('deadline')[:5]
        
        pending_tasks_count = Assignment.objects.filter(group__in=student_groups).exclude(submissions__student=user).count()
        
        # Attendance rate
        total_attendance = Attendance.objects.filter(student=user).count()
        present_attendance = Attendance.objects.filter(student=user, status='present').count()
        attendance_rate = int((present_attendance / total_attendance) * 100) if total_attendance > 0 else 0
        
        # Payments
        recent_payments = Payment.objects.filter(student=user).order_by('-created_at')[:5]
        
        # Schedule with attendance and assignment status
        from django.utils import timezone
        from datetime import timedelta

        schedule_slots = Schedule.objects.filter(group__enrollments__student=user).select_related('group', 'group__course', 'group__teacher').order_by('day_of_week', 'start_time')

        today = timezone.now().date()
        schedule_data = []

        for slot in schedule_slots:
            # Calculate the date for this schedule's day_of_week
            current_day_of_week = today.weekday()  # Monday=0, Sunday=6
            target_day_of_week = slot.day_of_week

            # Calculate days difference
            days_diff = (target_day_of_week - current_day_of_week) % 7
            if days_diff == 0:
                slot_date = today
                is_passed = False
            else:
                if days_diff <= current_day_of_week:
                    slot_date = today - timedelta(days=current_day_of_week - target_day_of_week)
                else:
                    slot_date = today - timedelta(days=(7 - days_diff))

                # Check if this slot is in the past
                is_passed = slot_date < today

            # Get attendance for this slot
            attendance = Attendance.objects.filter(
                student=user,
                schedule=slot,
                date=slot_date
            ).first()

            # Get assignments for this slot
            assignments = Assignment.objects.filter(
                schedule=slot,
                status='published'
            ).select_related('group')

            assignment_statuses = []
            for assignment in assignments:
                submission = Submission.objects.filter(
                    assignment=assignment,
                    student=user
                ).first()

                assignment_statuses.append({
                    'title': assignment.title,
                    'submitted': submission is not None,
                    'assignment_id': assignment.id,
                    'submission_id': submission.id if submission else None,
                })

            schedule_data.append({
                'slot': slot,
                'date': slot_date,
                'is_passed': is_passed,
                'attendance': attendance,
                'assignments': assignment_statuses,
            })

        # Sort: upcoming first, then past
        schedule_data.sort(key=lambda x: (x['is_passed'], x['slot'].day_of_week, x['slot'].start_time))

        ctx.update({
            "enrollments": enrollments,
            "enrolled_groups_count": enrolled_groups_count,
            "pending_tasks_count": pending_tasks_count,
            "attendance_rate": attendance_rate,
            "pending_assignments": pending_assignments,
            "recent_payments": recent_payments,
            "balance": user.balance,
            "schedule": schedule_data,
        })
    elif user.role == 'admin':
        students_count = User.objects.filter(role='student').count()
        teachers_count = User.objects.filter(role='teacher').count()
        categories = Category.objects.all()

        ctx.update({
            'groups': Group.objects.all().select_related('course', 'session', 'teacher'),
            'sessions': Session.objects.all().select_related('course'),
            'courses': Course.objects.all(),
            'categories': categories,
            'students_count': students_count,
            'teachers_count': teachers_count,
        })
    else:
        ctx.update({
            "enrolled_groups_count": 0,
            "pending_tasks_count": 0,
            "attendance_rate": 0,
            "student_feed": [],
            "my_groups_count": 0,
            "total_students_count": 0,
            "pending_reviews_count": 0,
            "teacher_feed": [],
        })
    return ctx
