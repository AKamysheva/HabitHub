"""
URL configuration for habithub project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from habits import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.HomePageView.as_view(), name='home'),
    path('goals/', views.GoalsView.as_view(), name='goals'),
    path('goals/add-goal/', views.AddGoal.as_view(), name='add-goal'),
    path('goals/archive-goal/<int:goal_id>/', views.archivegoal, name='archive-goal'),
    path('goals/delete-goal/<int:goal_id>/', views.delete_goal, name='delete-goal'),
    path('habits/', include('habits.urls')),
    path('users/', include('users.urls', namespace='users')),
    path('progress/', views.ProgressView.as_view(), name='progress'),
    path('feedback/', views.FeedbackView.as_view(), name='feedback'),
    path('feedback/answer-feedback/', TemplateView.as_view(template_name='habits/answer_feedback.html'), name='feedback-answer'),
    path('', include('pwa.urls')),
]

if settings.DEBUG:
    from debug_toolbar.toolbar import debug_toolbar_urls
    urlpatterns += debug_toolbar_urls()

admin.site.site_header = 'Панель администрирования'
admin.site.index_title = 'HabitHub'