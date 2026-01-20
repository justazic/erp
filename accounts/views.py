from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View

from .forms import LoginForm


# Create your views here.

class LoginView(View):
    def get( self, request ):
        return render(request, 'auth/login.html')

    def post( self, request ):
        form = LoginForm(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('/')

        return render(request, 'auth/login.html', {
            'form': form,
            'error': 'Login yoki parol xato',
            },
                      )


class LogoutView(View):
    def get( self, request ):
        logout(request)
        return redirect('/accounts/login/')


class ProfileUpdateView(LoginRequiredMixin, View):
    def get( self, request ):
        return render(request, 'accounts/profile.html')

    def post( self, request ):
        user = request.user
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')

        if request.FILES.get('avatar'):
            user.avatar = request.FILES.get('avatar')
        user.save()
        return redirect('profile')


class PasswordChangeView(LoginRequiredMixin, View):
    def get( self, request ):
        return render(request, 'accounts/password_change.html')

    def post( self, request ):
        if not request.user.check_password(request.POST.get('old_password')):
            return render(request, 'accounts/password_change.html', {
                'error': "Eski parol xatp!",
                },
                          )

        request.user.set_password(request.POST.get('new_password'))
        request.user.save()
        update_session_auth_hash(request, request.user)
        return redirect('profile')
