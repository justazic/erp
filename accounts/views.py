from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import TemplateView

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
      return render(request, 'dashboards/teacher.html')
    if user.role == 'student':
      return render(request, 'dashboards/student.html')
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
    return [ "dashboard.html" ]

  def get_context_data( self, **kwargs ):
    ctx = super().get_context_data(**kwargs)
    user = self.request.user
    ctx.update({
      "enrolled_groups_count": 0,
      "pending_tasks_count": 0,
      "attendance_rate": 0,
      "student_feed": [ ],
      "my_groups_count": 0,
      "total_students_count": 0,
      "pending_reviews_count": 0,
      "teacher_feed": [ ],
      }, )
    if user.role == 'teacher':
      ctx[ "teacher_feed" ] = [ {
        "title": "Check submissions",
        "sub": "Review latest student submissions",
        }, {
        "title": "Take attendance",
        "sub": "Mark today's attendance for your groups",
        }, ]
    elif user.role == 'student':
      ctx[ "student_feed" ] = [ {
        "title": "Continue learning",
        "sub": "Open your enrolled courses",
        }, {
        "title": "Submit tasks",
        "sub": "Complete pending assignments",
        }, ]
    return ctx
