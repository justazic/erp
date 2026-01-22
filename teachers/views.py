from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from accounts.models import User
from courses.models import Group
from students.models import Enrollment

class AdminTeacherListView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role == 'admin'

    def get(self, request):
        teachers = User.objects.filter(role='teacher').order_by('username')
        return render(request, 'teachers/admin_list.html', {
            'teachers': teachers,
        })

class AdminTeacherCreateView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role == 'admin'

    def get(self, request):
        return render(request, 'teachers/admin_form.html', {})

    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            return render(request, 'teachers/admin_form.html', {
                'error': 'Username already exists',
            })

        teacher = User.objects.create_user(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            password=password,
            role='teacher'
        )
        return redirect('teachers:detail', pk=teacher.id)

class AdminTeacherEditView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role == 'admin'

    def get(self, request, pk):
        teacher = get_object_or_404(User, pk=pk, role='teacher')
        return render(request, 'teachers/admin_form.html', {
            'teacher': teacher,
        })

    def post(self, request, pk):
        teacher = get_object_or_404(User, pk=pk, role='teacher')

        teacher.email = request.POST.get('email', teacher.email)
        teacher.first_name = request.POST.get('first_name', teacher.first_name)
        teacher.last_name = request.POST.get('last_name', teacher.last_name)
        teacher.phone = request.POST.get('phone', teacher.phone)

        password = request.POST.get('password')
        if password:
            teacher.set_password(password)

        teacher.save()
        return redirect('teachers:detail', pk=teacher.id)

class AdminTeacherDeleteView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role == 'admin'

    def post(self, request, pk):
        teacher = get_object_or_404(User, pk=pk, role='teacher')
        teacher.delete()
        return redirect('teachers:admin_list')

class TeacherListView(View):
    def get(self, request, pk):
        teacher = get_object_or_404(User, pk=pk, role='teacher')
        return render(request, 'teachers/detail.html', {
            'teacher': teacher,
        })

class MyGroupsListView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.role != 'teacher':
            return redirect('/')
        groups = Group.objects.filter(teacher=request.user).select_related('course', 'session')
        return render(request, 'teachers/my_groups.html', {
            'groups': groups,
        })

class GroupStudentsListView(LoginRequiredMixin, View):
    def get(self, request, group_id):
        group = get_object_or_404(Group, id=group_id)
        if request.user.role != 'teacher' and not request.user.is_staff:
            return redirect('/')
        
        enrollments = Enrollment.objects.filter(
            group=group,
            status='studying'
        ).select_related('student')
        
        return render(request, 'teachers/group_students.html', {
            'group': group,
            'enrollments': enrollments,
        })
