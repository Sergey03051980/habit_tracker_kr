from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class HabitModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
    
    def test_habit_creation(self):
        habit = Habit.objects.create(
            user=self.user,
            name='Утренняя зарядка',
            place='Дом',
            time='07:00:00',
            action='15 минут упражнений',
            duration=60
        )
        self.assertEqual(str(habit), 'Утренняя зарядка')
        self.assertEqual(habit.user, self.user)
    
    def test_pleasant_habit(self):
        habit = Habit.objects.create(
            user=self.user,
            name='Чтение книги',
            duration=30,
            is_pleasant=True
        )
        self.assertTrue(habit.is_pleasant)
