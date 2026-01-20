from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Course, Group, Comment
from teachers.models import Teacher


class CourseCreateView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.role != 'admin':
            return redirect('/')
        return render(request, 'courses/course_create.html')

    def post(self, request):
        if request.user.role != 'admin':
            return redirect('/')

        Course.objects.create(
            name=request.POST.get('name')
        )
        return redirect('/courses/')


class CourseListView(LoginRequiredMixin, View):
    def get(self, request):
        courses = Course.objects.all()
        return render(
            request,
            'courses/course_list.html',
            {'courses': courses}
        )


class GroupCreateView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.role != 'admin':
            return redirect('/')

        courses = Course.objects.all()
        teachers = Teacher.objects.all()

        return render(
            request,
            'courses/group_create.html',
            {
                'courses': courses,
                'teachers': teachers
            }
        )

    def post(self, request):
        if request.user.role != 'admin':
            return redirect('/')

        Group.objects.create(
            name=request.POST.get('name'),
            course_id=request.POST.get('course'),
            teacher_id=request.POST.get('teacher')
        )
        return redirect('/courses/groups/')


class GroupListView(LoginRequiredMixin, View):
    def get(self, request):
        groups = Group.objects.select_related('course', 'teacher')
        return render(
            request,
            'courses/group_list.html',
            {'groups': groups}
        )


class CommentCreateView(LoginRequiredMixin, View):
    def post(self, request):
        Comment.objects.create(
            user=request.user,
            text=request.POST.get('text')
        )
        return redirect(request.META.get('HTTP_REFERER', '/'))

