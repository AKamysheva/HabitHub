from django.test import TestCase
from habits.models import Habit, Goal, CustomUser
from habits.forms import AddHabitForm, AddGoalForm, FeedbackForm

class HabitsFormsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser.objects.create_user(username='testuser', password='TestPassword')
        cls.habit2 = Habit.objects.create(user=cls.user, name='Excercise', frequency='Every day')

    def test_habit_form_valid(self):
        habit_form = AddHabitForm(data={'name':'Reading', 'frequency': 'Every day'}, user=self.user.id)
        self.assertTrue(habit_form.is_valid())
        habit = habit_form.save()
        self.assertEqual(habit.name, 'Reading') 
        self.assertEqual(habit.frequency, 'Every day') 
        self.assertEqual(habit.user, self.user)

    def test_habit_form_invalid(self):
        habit_form = AddHabitForm(data={})
        self.assertFalse(habit_form.is_valid()) 
        self.assertEqual(len(habit_form.errors), 2)

    def test_goal_form_valid(self):
        goal_form = AddGoalForm(data={'habit': self.habit2, 'description': 'Test goal', 'target_date': '15-12-2024'}, user=self.user)
        self.assertTrue(goal_form.is_valid())
        goal = goal_form.save()
        self.assertEqual(goal.description, 'Test goal')
        self.assertEqual(goal.target_date, '15-12-2024')

    def test_goal_form_invalid(self):
        goal_form = AddGoalForm(data={})
        self.assertFalse(goal_form.is_valid()) 
        self.assertEqual(len(goal_form.errors), 3)

    def test_feedback_form(self):
        feedback_form = FeedbackForm(data={'feedback': 'This is test feedback message'})
        self.assertTrue(feedback_form.is_valid())

    

    
