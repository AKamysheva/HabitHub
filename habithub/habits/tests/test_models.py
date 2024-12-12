from django.test import TestCase
from habits.models import Habit, Goal, CustomUser
from django.utils import timezone


class HabitAndGoalTestClass(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser.objects.create_user(username='testuser', password='TestPassword')
        cls.habit = Habit.objects.create(user=cls.user, name='Reading', frequency='Every day')
        cls.goal = Goal.objects.create(habit=cls.habit, user=cls.user, description='Test goal', target_date='2024-12-31')
        cls.goal_past = Goal.objects.create(habit=cls.habit, user=cls.user, description='Test goal past', target_date='2024-12-31', created_date=timezone.now().date() - timezone.timedelta(days=30))
        cls.goal_future = Goal.objects.create(habit=cls.habit, user=cls.user, description='Test goal future', target_date=timezone.now().date() - timezone.timedelta(days=1))

    def test_habit_creation(self):
        habit = Habit.objects.get(name='Reading')
        self.assertEqual(habit.user.username, 'testuser')
        self.assertEqual(habit.frequency, 'Every day')
        self.assertEqual(habit.status, 'Активная')

    def test_goal_creation(self):
        goal = Goal.objects.get(description='Test goal')
        self.assertEqual(goal.user.username, 'testuser')
        self.assertEqual(goal.target_date, '2024-12-31')
        self.assertEqual(goal.status, 'Активная')
    
    def test_goal_progress(self):
        goal= Goal.objects.get(description='Test goal')
        progress = goal.get_progress_percentage()
        self.assertEqual(progress, 0)

    def test_goal_past_progress(self):
        goal = Goal.objects.get(description='Test goal past')
        progress = goal.get_progress_percentage()

        total_duration = (goal.target_date - goal.created_date).days
        time = (timezone.now().date() - goal.created_date).days
        expected_progress = min((time / total_duration) * 100, 100)
        self.assertEqual(progress, expected_progress, delta=0.1)

    def test_goal_future_progress(self):
        goal = Goal.objects.get(description='Test goal future')
        progress = goal.update_status()
        self.assertEqual(progress, 100)
        self.assertEqual(goal.status, Goal.Status.COMPLETED)

    def test_frequency_status_max_length(self):
        habit = Habit.objects.get(name='Reading')
        max_length = habit._meta.get_field('frequency').max_length
        max_length_status = habit._meta.get_field('status').max_length
        self.assertEqual(max_length, 30)
        self.assertEqual(max_length_status, 20)


    




    
