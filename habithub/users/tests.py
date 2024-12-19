from django.test import TestCase
from habits.models import CustomUser

class CustomUserTestClass(TestCase):
    def test_user_creation(self):
        user = CustomUser.objects.create_user(username='testuser', password='TestPassword')
        self.assertEqual(user.username, 'testuser')
        self.assertTrue(user.check_password('TestPassword'))
