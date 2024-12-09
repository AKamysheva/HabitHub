from django.urls import path
from . import views

urlpatterns = [
    path('', views.HabitsView.as_view(), name='habits'),
    path('add-habit/', views.AddHabit.as_view(), name='add-habit'),
    path('archive-habit/<int:habit_id>/', views.archivehabit, name='archive-habit'),
    path('delete-habit/<int:habit_id>/', views.delete_habit, name='delete-habit'),
    path('restore-habit/<int:habit_id>/', views.restore_habit, name='restore-habit'),
]