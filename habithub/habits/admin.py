from django.contrib import admin
from .models import * 


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name', 'status', 'frequency', 'created_date')
    list_display_links = ('user', 'name')
    ordering = ['user', 'created_date']

@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'habit', 'description', 'status', 'created_date', 'target_date')
    list_display_links = ('user', 'habit', 'description')

#admin.site.register(Habit, HabitAdmin)
