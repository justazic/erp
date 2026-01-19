from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.models import User
from .models import Student
# Create your views here.


class StudentCreateView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'students/create.html')
    
    def post(self, request):
        user = User.objects.create_user(
            username=request.POST.get('username'),
            password=request.POST.get('password'),
            role='student'
        )
        
        Student.objects.create(
            user=user,
            phone=request.POST.get('phone'),
            address=request.POST.get('addres')                   
        )
        return redirect('/')   
    
    
class StudentListView(LoginRequiredMixin, View):
    def get(self, request):
        students = Student.objects.all()
        return render(request, 'students/list.html', {'students', students})
    