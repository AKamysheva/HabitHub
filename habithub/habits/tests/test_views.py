from django.test import TestCase
from habits.models import Habit, Goal, CustomUser, Remainders
from django.urls import reverse
from datetime import date, time

class ViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser.objects.create_user(username='testuser', password='TestPassword')
        cls.habit1 = Habit.objects.create(user=cls.user, name='Reading', frequency='Every day')
        cls.habit2 = Habit.objects.create(user=cls.user, name='Excercise', frequency='Every day')
        cls.goal1 = Goal.objects.create(habit=cls.habit1, user=cls.user, description='Test goal', target_date='2025-01-31')

    def setUp(self):
        self.client.login(username='testuser', password='TestPassword')

    def test_habit_list_view(self):
        response = self.client.get('/habits/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'habits/habits.html')
        self.assertContains(response, 'Reading')
        self.assertContains(response, 'Excercise')

    def test_habit_add_view(self):
        response = self.client.post(reverse('add-habit'), {'user': self.user.id, 'name': 'Медитация', 'frequency':'Каждый день'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Habit.objects.count(), 3)
        new_habit = Habit.objects.get(name='Медитация')
        self.assertEqual(new_habit.frequency, 'Каждый день') 
        self.assertEqual(new_habit.user, self.user)

    def test_habit_archive(self):
        response = self.client.post(reverse('archive-habit', kwargs={'habit_id': self.habit1.id}))
        self.habit1.refresh_from_db()
        self.assertEqual(self.habit1.status, Habit.Status.ARCHIVED)
        self.assertRedirects(response, '/habits/')

    def test_habit_delete(self):
        response = self.client.post(reverse('delete-habit', kwargs={'habit_id': self.habit1.id}))
        self.assertFalse(Habit.objects.filter(id=self.habit1.id).exists())
        self.assertRedirects(response, '/habits/')

    def test_habit_restore(self):
        self.habit2.status = Habit.Status.ARCHIVED
        self.habit2.save()
        response = self.client.post(reverse('restore-habit', kwargs={'habit_id': self.habit2.id}))
        self.habit2.refresh_from_db()
        self.assertEqual(self.habit2.status, Habit.Status.ACTIVE)
        self.assertRedirects(response, '/habits/')
   
    def test_goal_list_view(self):
        response = self.client.get(reverse('goals'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'habits/goals_lst.html')
        self.assertContains(response, 'Test goal')

    def test_goal_add_view(self):
        response = self.client.post(reverse('add-goal'), {'user': self.user.id, 'habit': self.habit2.id, 'description': 'Test goal2', 'target_date': '2024-12-30'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Goal.objects.count(), 2)
        new_goal = Goal.objects.get(description='Test goal2')
        self.assertEqual(new_goal.target_date, date(2024, 12, 30))
        self.assertEqual(new_goal.user, self.user)

    def test_goal_delete(self):
        goal2 = Goal.objects.create(habit=self.habit1, user=self.user, description='Test goal to delete', target_date='2024-12-28')
        response = self.client.post(reverse('delete-goal', kwargs={'goal_id': goal2.id}))
        self.assertFalse(Goal.objects.filter(id=goal2.id).exists())
        self.assertRedirects(response, reverse('goals'))

    def test_feedback(self):
        response = self.client.get('/feedback/')
        self.assertEqual(response.status_code, 200)
    
    def test_progress(self):
        response = self.client.get('/progress/')
        self.assertEqual(response.status_code, 200)

    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_set_reminder_view(self):
        user_timezone = 'Europe/Moscow'
        response = self.client.post(reverse('set-reminder', kwargs={'habit_id': self.habit2.id}), data={'habit': self.habit2.id, 'reminder_time': time(12, 0), 'reminder_frequency': 'monthly', 'timezone': user_timezone})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Remainders.objects.count(), 1)
        reminder = Remainders.objects.first()
        self.assertEqual(reminder.habit, self.habit2)
        self.assertEqual(reminder.reminder_time, time(12, 0))
        self.assertEqual(reminder.reminder_frequency, 'monthly')

       



