from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.HabitsView.as_view(), name='habits'),
    path('add-habit/', views.AddHabit.as_view(), name='add-habit'),
    path('archive-habit/<int:habit_id>/', views.archivehabit, name='archive-habit'),
    path('delete-habit/<int:habit_id>/', views.delete_habit, name='delete-habit'),
    path('restore-habit/<int:habit_id>/', views.restore_habit, name='restore-habit'),
    path('set-reminders/<int:habit_id>/', views.SetReminderView.as_view(), name='set-reminder'),
    path('set-reminders/answer-reminder/', TemplateView.as_view(template_name='habits/answer_reminder.html'), name='reminder-answer'),
    path('delete-reminder/<int:reminder_id>/', views.delete_reminder, name='delete-reminder'),
]