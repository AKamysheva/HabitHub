from django.db import models
from django.utils import timezone
from users.models import CustomUser


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
    
    def get_progress(self):
        pass

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
        if total_duration == 0:
            return 100
        elif total_duration > 0:
            progress = (time / total_duration) * 100
            return min(progress, 100)
        return 0
    
    def update_status(self):
        progress = self.get_progress_percentage()
        if progress >= 100 and not Goal.Status.ARCHIVED:
            self.status = Goal.Status.COMPLETED
            self.save()
        return progress

    class Meta:
        verbose_name = 'Цели'
        verbose_name_plural = 'Цели'



class Remainders(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Пользователь')
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, verbose_name='Привычка')
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE, verbose_name='Цель')
    reminder_time = models.TimeField(blank=True, verbose_name='Время напоминания')
    reminder_frequency = models.CharField(max_length=30, blank=True, verbose_name='Частота напоминаний')
    is_active = models.BooleanField(default=False, verbose_name='Активно')

