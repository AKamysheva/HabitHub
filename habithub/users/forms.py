from typing import Any
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from .models import CustomUser

class CustomUserRegisterForm(UserCreationForm):
    email = forms.EmailField(label='E-mail', required=True)
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput())

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('Такой email уже существует!')
        return email

class CustomUserAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'password')
    
class ProfileCustomUserForm(forms.ModelForm):
    username = forms.CharField(disabled=True)
    email = forms.CharField(disabled=True)
   
    class Meta:
        model = CustomUser
        fields = ('username', 'email')

class CustomUserChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(label='Старый пароль', widget=forms.PasswordInput())
    new_password1 = forms.CharField(label='Новый пароль', widget=forms.PasswordInput())
    new_password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput())