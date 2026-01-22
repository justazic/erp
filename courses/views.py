from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Avg, Count, Q
from django.http import HttpResponseRedirect, JsonResponse
from .models import Course, Category, Comment, Group, Session
from accounts.models import User
from students.models import Enrollment
from teachers.models import TeacherCourse

from django.utils import timezone
from decimal import Decimal
from finance.models import Payment
import uuid
import datetime
import json

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role == 'admin'

class GroupCreateView(AdminRequiredMixin, View):
    def get(self, request):
        courses = Course.objects.all()
        sessions = Session.objects.all()
        teachers = User.objects.filter(role='teacher')
        return render(request, 'courses/admin/group_form.html', {
            'courses': courses,
            'sessions': sessions,
            'teachers': teachers,
            'selected_course': request.GET.get('course'),
            'selected_session': request.GET.get('session'),
        })

    def post(self, request):
        Group.objects.create(
            name=request.POST.get('name'),
            course_id=request.POST.get('course'),
            session_id=request.POST.get('session'),
            teacher_id=request.POST.get('teacher')
        )
        return redirect('courses:admin_dashboard')

class SessionCreateView(AdminRequiredMixin, View):
    def get(self, request):
        courses = Course.objects.all()
        return render(request, 'courses/admin/session_form.html', {'courses': courses})

    def post(self, request):
        Session.objects.create(
            course_id=request.POST.get('course'),
            session_type=request.POST.get('session_type'),
            start_date=request.POST.get('start_date'),
            end_date=request.POST.get('end_date'),
            capacity=request.POST.get('capacity', 30)
        )
        return redirect('courses:admin_dashboard')

class GroupUpdateView(AdminRequiredMixin, View):
    def get(self, request, pk):
        group = get_object_or_404(Group, pk=pk)
        courses = Course.objects.all()
        sessions = Session.objects.all()
        teachers = User.objects.filter(role='teacher')

        from attendance.models import Schedule
        from tasks.models import Assignment
        from django.utils import timezone
        from datetime import datetime, time

        schedules = Schedule.objects.filter(group=group).order_by('day_of_week', 'start_time')

        today = timezone.now().date()
        today_weekday = today.weekday()

        schedules_sorted = []
        for schedule in schedules:
            day_diff = (schedule.day_of_week - today_weekday) % 7
            if day_diff == 0:
                is_upcoming = timezone.now().time() < schedule.start_time
            else:
                is_upcoming = day_diff > 0 or day_diff < 0
            schedule.is_upcoming = is_upcoming
            schedules_sorted.append(schedule)

        schedules_sorted.sort(key=lambda x: (not x.is_upcoming, x.day_of_week, x.start_time))

        assignments = Assignment.objects.filter(group=group).order_by('-created_at')
        enrollments = Enrollment.objects.filter(group=group).select_related('student')

        return render(request, 'courses/admin/group_detail.html', {
            'group': group,
            'courses': courses,
            'sessions': sessions,
            'teachers': teachers,
            'schedules': schedules,
            'schedules_sorted': schedules_sorted,
            'assignments': assignments,
            'enrollments': enrollments,
        })

    def post(self, request, pk):
        group = get_object_or_404(Group, pk=pk)
        group.name = request.POST.get('name')
        group.course_id = request.POST.get('course')
        group.session_id = request.POST.get('session')
        group.teacher_id = request.POST.get('teacher')
        group.save()
        return redirect('courses:admin_dashboard')

class GroupDeleteView(AdminRequiredMixin, View):
    def post(self, request, pk):
        group = get_object_or_404(Group, pk=pk)
        group.delete()
        return redirect('courses:admin_dashboard')

class SessionUpdateView(AdminRequiredMixin, View):
    def get(self, request, pk):
        session = get_object_or_404(Session, pk=pk)
        courses = Course.objects.all()
        groups = session.groups.all().annotate(student_count=Count('enrollments'))

        unassigned_students = Enrollment.objects.filter(
            session=session,
            group__isnull=True
        ).select_related('student')

        session_students = Enrollment.objects.filter(
            session=session
        ).select_related('student', 'group')

        return render(request, 'courses/admin/session_detail.html', {
            'session': session,
            'courses': courses,
            'groups': groups,
            'unassigned_students': unassigned_students,
            'session_students': session_students
        })

    def post(self, request, pk):
        session = get_object_or_404(Session, pk=pk)

        if "update_session" in request.POST:
            session.course_id = request.POST.get('course')
            session.session_type = request.POST.get('session_type')
            session.start_date = request.POST.get('start_date')
            session.end_date = request.POST.get('end_date')
            session.capacity = request.POST.get('capacity', 30)
            session.save()
            return redirect('courses:admin_dashboard')

        elif "assign_student" in request.POST:
            student_id = request.POST.get('student_id')
            if User.objects.filter(id=student_id, role='student').exists():
                Enrollment.objects.get_or_create(
                    student_id=student_id,
                    course=session.course,
                    session=session,
                    defaults={'status': 'studying'}
                )
            return redirect('courses:session_update', pk=pk)

        elif "remove_student" in request.POST:
            student_id = request.POST.get('student_id')
            Enrollment.objects.filter(student_id=student_id, session=session).delete()
            return redirect('courses:session_update', pk=pk)

        return redirect('courses:session_update', pk=pk)

class SessionDeleteView(AdminRequiredMixin, View):
    def post(self, request, pk):
        session = get_object_or_404(Session, pk=pk)
        session.delete()
        return redirect('courses:admin_dashboard')

class CourseCreateView(AdminRequiredMixin, View):
    def get(self, request):
        categories = Category.objects.all()
        selected_category_id = request.GET.get('category')
        return render(request, 'courses/admin/course_form.html', {
            'categories': categories,
            'selected_category_id': selected_category_id
        })

    def post(self, request):
        Course.objects.create(
            name=request.POST.get('name'),
            category_id=request.POST.get('category'),
            price=request.POST.get('price'),
            small_description=request.POST.get('small_description'),
            large_description=request.POST.get('large_description')
        )
        return redirect('courses:admin_dashboard')

class CourseUpdateView(AdminRequiredMixin, View):
    def get(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        categories = Category.objects.all()

        return render(request, 'courses/admin/course_detail.html', {
            'course': course,
            'categories': categories
        })

    def post(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        course.name = request.POST.get('name')
        course.category_id = request.POST.get('category')
        course.price = request.POST.get('price')
        course.small_description = request.POST.get('small_description')
        course.large_description = request.POST.get('large_description')
        course.save()
        return redirect('courses:admin_dashboard')

class CourseDeleteView(AdminRequiredMixin, View):
    def post(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        course.delete()
        return redirect('courses:admin_dashboard')

class CategoryCreateView(AdminRequiredMixin, View):
    def get(self, request):
        return render(request, 'courses/admin/category_form.html')

    def post(self, request):
        Category.objects.create(name=request.POST.get('name'))
        return redirect('courses:admin_dashboard')

class CategoryUpdateView(AdminRequiredMixin, View):
    def get(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        return render(request, 'courses/admin/category_detail.html', {'category': category})

    def post(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        category.name = request.POST.get('name')
        category.save()
        return redirect('courses:admin_dashboard')

class CategoryDeleteView(AdminRequiredMixin, View):
    def post(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        category.delete()
        return redirect('courses:admin_dashboard')

class AdminDashboardView(AdminRequiredMixin, View):
    def get(self, request):
        groups = Group.objects.all().select_related('course', 'session', 'teacher').annotate(student_count=Count('enrollments'))
        sessions = Session.objects.all().select_related('course')
        courses = Course.objects.all().select_related('category')
        categories = Category.objects.all()
        students_count = User.objects.filter(role='student').count()
        teachers_count = User.objects.filter(role='teacher').count()
        return render(request, 'courses/admin/dashboard.html', {
            'groups': groups,
            'sessions': sessions,
            'courses': courses,
            'categories': categories,
            'students_count': students_count,
            'teachers_count': teachers_count
        })

class AdminStudentListView(AdminRequiredMixin, View):
    def get(self, request):
        search = request.GET.get('search', '')
        students = User.objects.filter(role='student').prefetch_related('enrollments')
        if search:
            students = students.filter(
                Q(username__icontains=search) |
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(email__icontains=search)
            )
        return render(request, 'courses/admin/student_list.html', {
            'students': students,
            'search': search
        })

class AdminStudentDetailView(AdminRequiredMixin, View):
    def get(self, request, pk):
        student = get_object_or_404(User, pk=pk, role='student')
        enrollments = Enrollment.objects.filter(student=student).select_related('course', 'session', 'group')
        payments = Payment.objects.filter(student=student).order_by('-created_at')
        return render(request, 'courses/admin/student_detail.html', {
            'student': student,
            'enrollments': enrollments,
            'payments': payments
        })

class AdminStudentCreateView(AdminRequiredMixin, View):
    def get(self, request):
        return render(request, 'courses/admin/student_form.html')

    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        if User.objects.filter(username=username).exists():
            return render(request, 'courses/admin/student_form.html', {'error': 'Username already exists'})

        student = User.objects.create(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            role='student'
        )
        student.set_password(password)
        student.save()
        return redirect('courses:admin_student_list')

class AdminStudentDepositView(AdminRequiredMixin, View):
    def post(self, request, pk):
        student = get_object_or_404(User, pk=pk, role='student')

        if "charge_monthly" in request.POST:
            enrollments = Enrollment.objects.filter(student=student, status='studying')
            total_charged = Decimal('0')
            for enr in enrollments:
                price = Decimal(enr.course.price or 0)
                monthly_fee = price / 3

                if student.balance >= monthly_fee:
                    student.balance -= monthly_fee
                    student.save()

                    Payment.objects.create(
                        student=student,
                        enrollment=enr,
                        amount=monthly_fee,
                        payment_type='monthly',
                        method='balance',
                        status='paid',
                        due_date=timezone.now().date(),
                        paid_date=timezone.now().date(),
                        reference_number=f"MON-{uuid.uuid4().hex[:8].upper()}",
                        notes=f"Monthly charge for {enr.course.name}"
                    )
                    total_charged += monthly_fee

            return redirect('courses:admin_student_detail', pk=pk)

        amount = Decimal(request.POST.get('amount', '0'))

        if amount <= 0:
            return redirect('courses:admin_student_detail', pk=pk)

        student.balance += amount
        student.save()

        Payment.objects.create(
            student=student,
            amount=amount,
            payment_type='deposit',
            method='cash',
            status='paid',
            due_date=timezone.now().date(),
            paid_date=timezone.now().date(),
            reference_number=f"DEP-{uuid.uuid4().hex[:8].upper()}",
            notes=f"Admin deposit: {request.POST.get('notes', '')}"
        )

        return redirect('courses:admin_student_detail', pk=pk)

class AdminGroupStudentsView(AdminRequiredMixin, View):
    def get(self, request, pk):
        group = get_object_or_404(Group, pk=pk)
        group_enrollments = Enrollment.objects.filter(group=group).select_related('student')

        available_students = Enrollment.objects.filter(
            session=group.session,
            course=group.course
        ).exclude(group=group).select_related('student')

        return render(request, 'courses/admin/group_students_manage.html', {
            'group': group,
            'group_enrollments': group_enrollments,
            'available_students': available_students
        })

    def post(self, request, pk):
        group = get_object_or_404(Group, pk=pk)
        action = request.POST.get('action')
        student_id = request.POST.get('student_id')

        if action == 'add':
            enrollment = get_object_or_404(Enrollment, student_id=student_id, course=group.course, session=group.session)
            enrollment.group = group
            enrollment.save()
        elif action == 'remove':
            enrollment = get_object_or_404(Enrollment, student_id=student_id, group=group)
            enrollment.group = None
            enrollment.save()

        return redirect('courses:admin_group_students', pk=pk)

class CourseListView(View):
  def get( self, request ):
    search = request.GET.get('search', '')
    category_id = request.GET.get('category')

    courses = Course.objects.prefetch_related("sessions", "category")

    if search:
        courses = courses.filter(
            Q(name__icontains=search) |
            Q(small_description__icontains=search) |
            Q(large_description__icontains=search)
        )

    if category_id:
        courses = courses.filter(category_id=category_id)

    categories = Category.objects.all()

    return render(request, "courses/list.html", {
      "courses": courses,
      "categories": categories,
      "active_category": int(category_id) if category_id and category_id.isdigit() else None,
      }, )


class CourseDetailCreateView(View):
  def get( self, request, pk ):
    course = get_object_or_404(Course, pk=pk)
    comments = Comment.objects.filter(course_id=pk).order_by("-created_at")
    total_reviews = Comment.objects.filter(course_id=pk).count()
    rating_avg = round(Comment.objects.filter(course_id=pk).aggregate(Avg("rating"))["rating__avg"] or 0, 1)
    teachercourses = TeacherCourse.objects.filter(course_id=pk).select_related("teacher")

    if request.user.is_authenticated:
      is_enrolled = Enrollment.objects.filter(student=request.user, course_id=pk).exists()
    else: is_enrolled = False

    rating_counts = { i: 0 for i in range(1, 6) }
    for c in comments:
      if 1 <= c.rating <= 5:
        rating_counts[ c.rating ] += 1

    rating_bars = [ ]
    for star in range(5, 0, -1):
      count = rating_counts.get(star, 0)
      percent = int((count / total_reviews) * 100) if total_reviews else 0
      rating_bars.append({
        "star": star,
        "count": count,
        "percent": percent,
        }
        )

    sessions = Session.objects.filter(course=course, is_active=True).prefetch_related('groups', 'groups__teacher')

    return render(request, "courses/detail.html", {
      "course": course,
      "comments": comments,
      'teachercourses': teachercourses,
      'total_reviews': total_reviews,
      'rating_avg': rating_avg,
      "rating_bars": rating_bars,
      'is_enrolled': is_enrolled,
      'is_authenticated': request.user.is_authenticated,
      'sessions': sessions,
      }, )

  def post(self, request, pk):
    if not request.user.is_authenticated or request.user.role != 'student':
        return redirect('accounts:login')

    course = get_object_or_404(Course, pk=pk)

    if "enroll" in request.POST:
        session_id = request.POST.get('session')
        group_id = request.POST.get('group')

        if not session_id or not group_id:
            return redirect('courses:detail', pk=pk)

        session = get_object_or_404(Session, id=session_id, course=course)
        group = get_object_or_404(Group, id=group_id, course=course, session=session)

        if Enrollment.objects.filter(student=request.user, course=course).exists():
             return redirect('accounts:dashboard')

        price = Decimal(course.price or 0)
        if request.user.balance < price:
            return redirect('courses:detail', pk=pk)

        request.user.balance -= price
        request.user.save()

        Enrollment.objects.create(
            student=request.user,
            course=course,
            session=session,
            group=group,
            status='studying'
        )

        Payment.objects.create(
            student=request.user,
            amount=price,
            payment_type='tuition',
            method='balance',
            status='paid',
            due_date=timezone.now().date(),
            paid_date=timezone.now().date(),
            reference_number=f"ENR-{uuid.uuid4().hex[:8].upper()}",
            notes=f"Enrollment in {course.name}"
        )

        return redirect('accounts:dashboard')

    elif "rating" in request.POST:
        Comment.objects.create(
            course=course,
            user=request.user,
            rating=request.POST.get('rating'),
            text=request.POST.get('text')
        )
        return redirect('courses:detail', pk=pk)

    return redirect('courses:detail', pk=pk)

class GroupStudentSearchAPIView(AdminRequiredMixin, View):
    """API endpoint for searching available students for a group"""
    def get(self, request, pk):
        group = get_object_or_404(Group, pk=pk)
        search_term = request.GET.get('q', '').lower().strip()

        enrolled_student_ids = Enrollment.objects.filter(group=group).values_list('student_id', flat=True)

        available_students = User.objects.filter(role='student').exclude(id__in=enrolled_student_ids)

        if search_term:
            available_students = available_students.filter(
                Q(first_name__icontains=search_term) |
                Q(last_name__icontains=search_term) |
                Q(username__icontains=search_term) |
                Q(email__icontains=search_term) |
                Q(id__iexact=search_term)
            )

        available_students = available_students[:20]

        students_data = [{
            'id': student.id,
            'name': student.get_full_name() or student.username,
            'email': student.email,
            'username': student.username
        } for student in available_students]

        return JsonResponse({'students': students_data})

class EnrollmentAddView(AdminRequiredMixin, View):
    def post(self, request, pk):
        """Add a student to a group"""
        group = get_object_or_404(Group, pk=pk)
        student_id = request.POST.get('student_id')
        search_term = request.POST.get('search_term', '')
        student = get_object_or_404(User, pk=student_id, role='student')

        if not Enrollment.objects.filter(student=student, group=group).exists():
            Enrollment.objects.create(
                student=student,
                group=group,
                course=group.course,
                session=group.session,
                status='active'
            )

        redirect_url = f"{redirect('courses:group_update', pk=pk).url}?tab=students"
        if search_term:
            import urllib.parse
            redirect_url += f"&search={urllib.parse.quote(search_term)}"

        return HttpResponseRedirect(redirect_url)


class EnrollmentRemoveView(AdminRequiredMixin, View):
    def post(self, request, pk):
        """Remove a student from a group"""
        enrollment = get_object_or_404(Enrollment, pk=pk)
        group_id = enrollment.group.id
        search_term = request.POST.get('search_term', '')
        enrollment.delete()

        redirect_url = f"{redirect('courses:group_update', pk=group_id).url}?tab=students"
        if search_term:
            import urllib.parse
            redirect_url += f"&search={urllib.parse.quote(search_term)}"

        return HttpResponseRedirect(redirect_url)