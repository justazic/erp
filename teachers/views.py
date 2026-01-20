from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.models import User
from .models import Teacher

class TeacherCreateView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.role != 'admin':
            return redirect('/')
        return render(request, 'teachers/create.html')

    def post(self, request):
        if request.user.role != 'admin':
            return redirect('/')

        user = User.objects.create_user(
            username=request.POST.get('username'),
            password=request.POST.get('password'),
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            role='teacher'
        )

        Teacher.objects.create(
            user=user,
            speciality=request.POST.get('speciality'),
            phone=request.POST.get('phone')
        )
        return redirect('/teachers/')


class TeacherListView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.role != 'admin':
            return redirect('/')

        teachers = Teacher.objects.all()
        return render(request, 'teachers/list.html', {'teachers': teachers})


class TeacherProfileView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.role != 'teacher':
            return redirect('/')

        teacher = request.user.teacher
        return render(request, 'teachers/profile.html', {'teacher': teacher})


class TeacherUpdateView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.role != 'teacher':
            return redirect('/')

        return render(
            request,
            'teachers/update.html',
            {'teacher': request.user.teacher}
        )

    def post(self, request):
        if request.user.role != 'teacher':
            return redirect('/')

        teacher = request.user.teacher
        teacher.speciality = request.POST.get('speciality')
        teacher.phone = request.POST.get('phone')
        teacher.bio = request.POST.get('bio')
        teacher.experience_year = request.POST.get('experience_years')
        teacher.save()

        return redirect('/teachers/profile/')


class TeacherDeleteView(LoginRequiredMixin, View):
    def post(self, request, teacher_id):
        if request.user.role != 'admin':
            return redirect('/')

        teacher = get_object_or_404(Teacher, id=teacher_id)
        teacher.user.delete()
        return redirect('/teachers/')