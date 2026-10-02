from django.shortcuts import render
from .models import UserRegister
from .forms import RegisterUserForm
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView,LogoutView
from django.urls import reverse_lazy

class RegisterUser(CreateView):
    model = UserRegister
    form_class = RegisterUserForm
    template_name = 'register/register.html'
    success_url = reverse_lazy('login')
    
class LoginUser(LoginView):
    template_name = 'register/login.html'
    next_page = reverse_lazy('profile_create')
    
    
class LogoutUser(LogoutView):
    next_page = reverse_lazy('login')
