from django.test import TestCase
from django.core import mail
from django.utils import timezone
from habits.models import Remainders, Habit
from habits.tasks import send_reminders, add_task_to_celery_beat
from users.models import CustomUser
from datetime import time, timedelta
from unittest.mock import patch
from django.core.mail import send_mail
from django.conf import settings
from django_celery_beat.models import PeriodicTask, CrontabSchedule

class ReminderTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', email='testuser@example.com', password='TestPassword')
        self.habit = Habit.objects.create(name='Test Habit', user=self.user)
        self.reminder = Remainders.objects.create(user=self.user, habit=self.habit, reminder_time=time(14, 0), reminder_frequency='daily', is_active=True)
        self.weekly_reminder = Remainders.objects.create(user=self.user, habit=self.habit, reminder_time=time(14, 0), reminder_frequency='weekly', is_active=True)
        self.monthly_reminder = Remainders.objects.create(user=self.user, habit=self.habit, reminder_time=time(9, 0), reminder_frequency='monthly', is_active=True)
        self.reminder.user_timezone = "Europe/Moscow"
        self.weekly_reminder.user_timezone = "Europe/Moscow"
        self.monthly_reminder.user_timezone = "Europe/Moscow"
        
        add_task_to_celery_beat(self.reminder)
        add_task_to_celery_beat(self.weekly_reminder)
        add_task_to_celery_beat(self.monthly_reminder)

    def test_daily_reminder_task_created(self):
        task = PeriodicTask.objects.filter(name=f'reminder_task_{self.reminder.id}')
        self.assertTrue(task.exists())

    def test_weekly_reminder_task_created(self):
        task = PeriodicTask.objects.filter(name=f'reminder_task_{self.weekly_reminder.id}')
        self.assertTrue(task.exists())

    def test_monthly_reminder_task_created(self):
        task = PeriodicTask.objects.filter(name=f'reminder_task_{self.monthly_reminder.id}')
        self.assertTrue(task.exists())
            
    def test_daily_reminder_task_parameters(self):
        task = PeriodicTask.objects.get(name=f'reminder_task_{self.reminder.id}')
        schedule = task.crontab
        self.assertEqual(schedule.day_of_month, '*')
        self.assertEqual(schedule.month_of_year, '*')
        self.assertEqual(schedule.day_of_week, '*')
    
    def test_weekly_reminder_task_parameters(self):
        task = PeriodicTask.objects.get(name=f'reminder_task_{self.weekly_reminder.id}')
        schedule = task.crontab
        self.assertEqual(schedule.day_of_week, '1') 
        self.assertEqual(schedule.day_of_month, '*')
        self.assertEqual(schedule.month_of_year, '*')

    def test_monthly_reminder_task_parameters(self):
        task = PeriodicTask.objects.get(name=f'reminder_task_{self.monthly_reminder.id}')
        schedule = task.crontab
        self.assertEqual(schedule.day_of_month, '1')
        self.assertEqual(schedule.month_of_year, '*')
        self.assertEqual(schedule.day_of_week, '*')

    def test_task_created_once(self):
        task_count = PeriodicTask.objects.filter(name=f'reminder_task_{self.reminder.id}').count()
        self.assertEqual(task_count, 1)

    @patch('django.utils.timezone.now', return_value=timezone.datetime(2025, 1, 13, 14, 0)) 
    @patch('habits.tasks.send_reminders.apply_async') 
    def test_weekly_task_execution(self, mock_apply_async, mock_now): 
        task = PeriodicTask.objects.get(name=f'reminder_task_{self.weekly_reminder.id}') 
        task_args = eval(task.args)
        send_reminders.apply_async(args=task_args) 
        mock_apply_async.assert_called_once_with(args=task_args)