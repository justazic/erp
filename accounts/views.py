from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.views import View

# Create your views here.

class LoginView(View):
    def get(self, request):
        return render(request, 'auth/login.html')
    
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user:
            login(request, user)
            return redirect('/')
        
        return render(request, 'auth/login.html', {'error': 'Login yoki parol xato'})
    
    
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('/login/')