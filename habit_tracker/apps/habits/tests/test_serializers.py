from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()

    def setUp(self):
        self.user = User.objects.create_user(
            email='serializer@test.com',
            password='test123'
        )
    
    def test_valid_habit(self):
        data = {
            'user': self.user.id,
            'name': 'Тестовая привычка',
            'duration': 60,
            'reward': 'Кофе'
        }
        self.assertTrue(serializer.is_valid())
    
    def test_duration_too_long(self):
        data = {
            'user': self.user.id,
            'name': 'Долгая привычка',
            'duration': 150  # > 120 секунд
        }
        self.assertFalse(serializer.is_valid())
        self.assertIn('duration', serializer.errors)
