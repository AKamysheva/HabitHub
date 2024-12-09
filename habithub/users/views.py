from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from .forms import CustomUserRegisterForm, CustomUserAuthenticationForm, ProfileCustomUserForm, CustomUserChangePasswordForm
from .models import CustomUser

class LoginCustomUser(LoginView):
    authentication_form = CustomUserAuthenticationForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Авторизация'}

    def get_success_url(self):
        return reverse_lazy('home')

class RegisterCustomUser(CreateView):
    form_class = CustomUserRegisterForm
    template_name = 'users/register.html'
    extra_context = {'title': 'Регистрация'}
    success_url = reverse_lazy('users:login')


class ProfileCustomUser(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = ProfileCustomUserForm
    template_name = 'users/profile.html'
    extra_context = {'title': 'Профиль пользователя'}

    def get_success_url(self):
        return reverse_lazy('users:profile')
    
    def get_object(self, queryset=None):
        return self.request.user
    
class CustomUserChangePassword(PasswordChangeView):
    form_class = CustomUserChangePasswordForm
    success_url = reverse_lazy('users:password_change_done')
    template_name = 'users/password_change_form.html'
    