from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.models import User
from .models import Student
# Create your views here.


class StudentCreateView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.role != 'admin':
            return redirect('/')
        return render(request, 'students/create.html')

    def post(self, request):
        if request.user.role != 'admin':
            return redirect('/')

        user = User.objects.create_user(
            username=request.POST.get('username'),
            password=request.POST.get('password'),
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            role='student'
        )

        Student.objects.create(
            user=user,
            phone=request.POST.get('phone'),
            address=request.POST.get('address'),
            birth_date=request.POST.get('birth_date') or None
        )
        return redirect('/students/')  
    
    
class StudentListView(LoginRequiredMixin, View):
    def get(self, request):
        students = Student.objects.all()
        return render(request, 'students/list.html', {'students': students})
    
    
class StudentProfileView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.role != 'student':
            return redirect('/')
        return render(
            request,
            'students/profile.html',
            {'student': request.user.student}
        )


class StudentUpdateView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.role != 'student':
            return redirect('/')
        return render(
            request,
            'students/update.html',
            {'student': request.user.student}
        )

    def post(self, request):
        if request.user.role != 'student':
            return redirect('/')

        user = request.user
        student = user.student

        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.save()

        student.phone = request.POST.get('phone')
        student.address = request.POST.get('address')
        student.birth_date = request.POST.get('birth_date') or None
        student.save()

        return redirect('/students/profile/')


class StudentToggleActiveView(LoginRequiredMixin, View):
    def post(self, request, student_id):
        if request.user.role != 'admin':
            return redirect('/')

        student = get_object_or_404(Student, id=student_id)
        student.active = not student.active
        student.save()
        return redirect('/students/')
