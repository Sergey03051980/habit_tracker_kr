"""
Простые тесты для проверки работы проекта.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Habit

User = get_user_model()


class HabitModelTest(TestCase):
    """Тесты модели привычек."""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_habit_creation(self):
        """Тест создания привычки."""
        habit = Habit.objects.create(
            user=self.user,
            name='Читать книгу',
            period='daily',
            duration=60
        )
        self.assertEqual(habit.name, 'Читать книгу')
        self.assertEqual(habit.duration, 60)
        self.assertEqual(habit.user, self.user)
    
    def test_duration_validation(self):
        """Тест валидации времени выполнения."""
        habit = Habit(
            user=self.user,
            name='Тест',
            period='daily',
            duration=150  # Больше 120 секунд
        )
        # Должна быть ошибка валидации
        from django.core.exceptions import ValidationError
        try:
            habit.full_clean()
            self.fail('Должна быть ошибка валидации')
        except ValidationError as e:
            self.assertIn('duration', e.message_dict)


class APITest(TestCase):
    """Базовый класс для API тестов."""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='apiuser',
            email='api@test.com',
            password='testpass123'
        )
        self.client.force_login(self.user)
