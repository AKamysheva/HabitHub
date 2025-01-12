from django.db import models
from django.utils import timezone
from users.models import CustomUser
from datetime import time


class AbstractModel(models.Model):
    class Meta:
        abstract = True

    class Status(models.TextChoices):
        ACTIVE = 'Активная', 'Активная' 
        COMPLETED = 'Достигнута', 'Достигнута' 
        ARCHIVED = 'В архиве', 'В архиве'
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Пользователь')
    status = models.CharField(max_length=20, choices=Status, default=Status.ACTIVE, verbose_name='Статус')
    created_date = models.DateField(auto_now_add=True, verbose_name='Дата создания')


class Habit(AbstractModel):   
    name = models.CharField(max_length=100, verbose_name='Название привычки')
    frequency = models.CharField(max_length=30, verbose_name='Частота выполнения')

    def __str__(self):
        return self.name
    
    def has_active_reminder(self): 
        return self.remainders.filter(is_active=True).exists()

    class Meta:
        verbose_name = 'Привычки'
        verbose_name_plural = 'Привычки'


class Goal(AbstractModel):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, verbose_name='Привычка')
    description = models.CharField(max_length=255, verbose_name='Описание цели')
    target_date = models.DateField(verbose_name='Дата достижения цели')

    def get_progress_percentage(self):
        total_duration = (self.target_date - self.created_date).days
        time = (timezone.now().date() - self.created_date).days
        if total_duration <= 0:
            return 100
        else:
            progress = (time / total_duration) * 100
            return min(progress, 100)
    
    def update_status(self):
        progress = self.get_progress_percentage()
        if progress >= 100 and self.status != Goal.Status.ARCHIVED:
            self.status = Goal.Status.COMPLETED
            self.save()

    class Meta:
        verbose_name = 'Цели'
        verbose_name_plural = 'Цели'



class Remainders(models.Model):
    FREQUENCY_CHOICES = [('daily', 'Ежедневно'), ('weekly', 'Еженедельно'), ('monthly', 'Ежемесячно')]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Пользователь')
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, verbose_name='Привычка', related_name='reminders')
    reminder_time = models.TimeField(blank=True, verbose_name='Время напоминания')
    reminder_frequency = models.CharField(max_length=30, choices=FREQUENCY_CHOICES, blank=True, verbose_name='Частота напоминаний')
    is_active = models.BooleanField(default=False, verbose_name='Активно')

    def __str__(self): 
        return f'{self.user.username} - {self.habit.name} - {self.reminder_time.replace(second=0, microsecond=0)}'

    def display_frequency_choices(self):
        return dict(self.FREQUENCY_CHOICES).get(self.reminder_frequency, self.reminder_frequency)
