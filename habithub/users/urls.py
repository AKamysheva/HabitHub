from django.urls import path
from django.contrib.auth.views import LogoutView, PasswordChangeDoneView
from . import views

app_name = 'users'

urlpatterns = [
    path('profile/', views.ProfileCustomUser.as_view(), name='profile'),
    path('login/', views.LoginCustomUser.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterCustomUser.as_view(), name='register'),
    path('password-change/', views.CustomUserChangePassword.as_view(), name='password_change'),
    path('password-change/done/', PasswordChangeDoneView.as_view(template_name='users/password_change_done.html'), name='password_change_done'),
]