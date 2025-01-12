from datetime import datetime
from celery import shared_task
from django.core.mail import send_mail
from habits.models import Remainders
from django.utils import timezone
from django.conf import settings
from django_celery_beat.models import CrontabSchedule, PeriodicTask
import pytz

@shared_task
def send_reminders(reminder_id):
    try:
        reminder = Remainders.objects.get(id=reminder_id)
        if reminder.is_active:
            display_frequency = reminder.display_frequency_choices()
            email_from = settings.EMAIL_HOST_USER
            send_mail(
                f'{display_frequency}е напоминание',
                f'У вас установлено напоминание для привычки: {reminder.habit.name}',
                email_from,
                [reminder.user.email],
                fail_silently=False
            )
    except Remainders.DoesNotExist:
        print(f"Напоминание с ID {reminder_id} не найдено")


def add_task_to_celery_beat(reminder):
    task_name = f'reminder_task_{reminder.id}'
    user_tz = pytz.timezone(reminder.user_timezone)
    
    now_date = timezone.localdate() 
    reminder_time = datetime.combine(now_date, reminder.reminder_time)
    reminder_time_user_tz = user_tz.localize(reminder_time)
    reminder_time_utc = reminder_time_user_tz.astimezone(pytz.UTC)

    minute = reminder_time_utc.minute
    hour = reminder_time_utc.hour

    schedule, _ = CrontabSchedule.objects.get_or_create(
        minute=minute, 
        hour=hour,
        day_of_month='1' if reminder.reminder_frequency == 'monthly' else '*',
        day_of_week='1' if reminder.reminder_frequency == 'weekly' else '*',
        )
    PeriodicTask.objects.update_or_create(
        name=task_name,
        defaults={'task': 'habits.tasks.send_reminders', 'crontab': schedule, 'args': f'[{reminder.id}]', 'enabled': True}
    )
