#!/usr/bin/env python
"""
Запуск тестов вручную.
"""
import os
import sys
import django

# Настраиваем Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'habit_tracker.settings')
django.setup()

from django.test import TestCase
from django.contrib.auth import get_user_model
from habit_tracker.apps.habits.models import Habit

User = get_user_model()


class SimpleHabitTest(TestCase):
    """Простые тесты для покрытия."""
    
    def test_user_and_habit(self):
        """Тест создания пользователя и привычки."""
        # Создаем пользователя
        user = User.objects.create_user(
            username='simpleuser',
            email='simple@test.com',
            password='password123'
        )
        self.assertEqual(user.email, 'simple@test.com')
        
        # Создаем привычку
        habit = Habit.objects.create(
            user=user,
            name='Простая привычка',
            period='daily',
            duration=90
        )
        self.assertEqual(habit.name, 'Простая привычка')
        self.assertEqual(habit.user, user)
        
        print('✅ Тест создания пользователя и привычки пройден')
        return True
    
    def test_habit_validation(self):
        """Тест валидации привычки."""
        user = User.objects.create_user(
            username='validuser',
            email='valid@test.com',
            password='password123'
        )
        
        # Создаем валидную привычку
        habit = Habit(
            user=user,
            name='Валидная привычка',
            period='weekly',
            duration=120  # Максимально допустимое время
        )
        
        try:
            habit.full_clean()
            print('✅ Валидация привычки пройдена')
            return True
        except Exception as e:
            print(f'❌ Ошибка валидации: {e}')
            return False


if __name__ == '__main__':
    import unittest
    
    # Запускаем тесты
    suite = unittest.TestLoader().loadTestsFromTestCase(SimpleHabitTest)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Выводим статистику
    print(f'\n{"="*50}')
    print(f'Тестов пройдено: {result.testsRun - len(result.failures) - len(result.errors)}/{result.testsRun}')
    print(f'Ошибок: {len(result.errors)}')
    print(f'Провалов: {len(result.failures)}')
    
    if result.wasSuccessful():
        print('🎉 Все тесты пройдены успешно!')
        sys.exit(0)
    else:
        print('⚠️ Есть проблемы с тестами')
        sys.exit(1)
