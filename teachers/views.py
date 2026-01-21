from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.models import User
from courses.models import Group
from students.models import Enrollment

class TeacherListView(View):
    def get(self, request, pk):
        teacher = get_object_or_404(User, pk=pk, role='teacher')
        return render(request, 'teachers/detail.html', { # Changed from list.html to detail.html as it takes a pk
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
        
        # In this system, enrollments are per course. Groups are also per course.
        # Usually, students in a group are those enrolled in the course AND assigned to that group.
        # However, the Enrollment model doesn't have a group field. 
        # Looking at Group model, it has course and session.
        # Enrollment model has course and session.
        
        enrollments = Enrollment.objects.filter(
            group=group,
            status='studying'
        ).select_related('student')
        
        return render(request, 'teachers/group_students.html', {
            'group': group,
            'enrollments': enrollments,
        })
