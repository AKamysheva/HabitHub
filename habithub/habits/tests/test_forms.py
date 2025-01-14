from django.test import TestCase
from habits.models import Habit, Goal, CustomUser, Remainders
from habits.forms import AddHabitForm, AddGoalForm, FeedbackForm, ReminderForm
from datetime import date, time

class HabitsFormsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser.objects.create_user(username='testuser', password='TestPassword')
        cls.habit2 = Habit.objects.create(user=cls.user, name='Excercise', frequency='Every day')

    def test_habit_form_valid(self):
        habit_form = AddHabitForm(data={'name':'Reading', 'frequency': 'Every day'})
        self.assertTrue(habit_form.is_valid())
        habit = habit_form.save(commit=False)
        habit.user = self.user 
        habit.save()

        self.assertEqual(habit.name, 'Reading') 
        self.assertEqual(habit.frequency, 'Every day') 
        self.assertEqual(habit.user, self.user)

    def test_habit_form_invalid(self):
        habit_form = AddHabitForm(data={})
        self.assertFalse(habit_form.is_valid()) 
        self.assertEqual(len(habit_form.errors), 2)

    def test_goal_form_valid(self):
        goal_form = AddGoalForm(data={'habit': self.habit2, 'description': 'Test goal', 'target_date': date(2024, 12, 15)}, initial={'user': self.user})
        self.assertTrue(goal_form.is_valid(), msg=goal_form.errors)
        goal = goal_form.save(commit=False)
        goal.user = self.user 
        self.assertEqual(goal.description, 'Test goal')
        self.assertEqual(goal.target_date, date(2024, 12, 15))

    def test_goal_form_invalid(self):
        goal_form = AddGoalForm(data={}, initial={'user': self.user})
        self.assertFalse(goal_form.is_valid()) 
        self.assertEqual(len(goal_form.errors), 3)

    def test_feedback_form(self):
        feedback_form = FeedbackForm(data={'feedback': 'This is test feedback message'})
        self.assertTrue(feedback_form.is_valid())

    def test_reminder_form(self):
        reminder_form = ReminderForm(data={'habit': self.habit2.id, 'reminder_time': time(10, 0), 'reminder_frequency': 'daily'}, user=self.user, habit=self.habit2)
        self.assertTrue(reminder_form.is_valid())
        reminder = reminder_form.save(commit=False)
        reminder.user = self.user
        reminder.save()
        self.assertEqual(Remainders.objects.count(), 1)
        self.assertEqual(reminder.habit, self.habit2)
        self.assertEqual(reminder.reminder_time, time(10, 0))

    

    
