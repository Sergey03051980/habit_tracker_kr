from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Habit, HabitCompletion

User = get_user_model()

class HabitModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            username='test@example.com'
        )
    
    def test_habit_creation(self):
        habit = Habit.objects.create(
            user=self.user,
            name='Test Habit',
            place='Home',
            time='10:00:00',
            action='Exercise',
            duration=60,
            is_public=False,
            is_pleasant=False,
            reward='Coffee'
        )
        self.assertEqual(str(habit), 'Test Habit')
        self.assertEqual(habit.user, self.user)
        self.assertEqual(habit.duration, 60)
    
    def test_pleasant_habit(self):
        habit = Habit.objects.create(
            user=self.user,
            name='Pleasant Habit',
            duration=30,
            is_pleasant=True
        )
        self.assertTrue(habit.is_pleasant)
        self.assertIsNone(habit.reward)

class HabitAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='api@example.com',
            password='apipass123',
            username='api@example.com'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        
        # Создаем тестовую привычку
        self.habit = Habit.objects.create(
            user=self.user,
            name='Test API Habit',
            place='Office',
            duration=90,
            reward='Tea'
        )
    
    def test_create_habit(self):
        data = {
            'name': 'New Habit',
            'place': 'Gym',
            'time': '08:00:00',
            'action': 'Workout',
            'duration': 45,
            'is_public': True,
            'is_pleasant': False,
            'reward': 'Protein Shake'
        }
        response = self.client.post('/api/habits/habits/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 2)
    
    def test_list_habits(self):
        response = self.client.get('/api/habits/habits/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_retrieve_habit(self):
        response = self.client.get(f'/api/habits/habits/{self.habit.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test API Habit')
    
    def test_update_habit(self):
        data = {'name': 'Updated Habit'}
        response = self.client.patch(f'/api/habits/habits/{self.habit.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.habit.refresh_from_db()
        self.assertEqual(self.habit.name, 'Updated Habit')
    
    def test_delete_habit(self):
        response = self.client.delete(f'/api/habits/habits/{self.habit.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.count(), 0)
    
    def test_complete_habit(self):
        response = self.client.post(f'/api/habits/habits/{self.habit.id}/complete/')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(HabitCompletion.objects.count(), 1)
    
    def test_public_habits(self):
        # Создаем публичную привычку
        Habit.objects.create(
            user=self.user,
            name='Public Habit',
            duration=60,
            is_public=True
        )
        
        # Тестируем без аутентификации
        self.client.logout()
        response = self.client.get('/api/habits/public/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class HabitValidationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='val@example.com',
            password='valpass123',
            username='val@example.com'
        )
    
    def test_duration_validation(self):
        from .serializers import HabitSerializer
        data = {
            'user': self.user.id,
            'name': 'Long Habit',
            'duration': 150  # > 120 секунд
        }
        serializer = HabitSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('duration', serializer.errors)
    
    def test_period_validation(self):
        from .serializers import HabitSerializer
        data = {
            'user': self.user.id,
            'name': 'Weekly Habit',
            'period': 10  # > 7 дней
        }
        serializer = HabitSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('period', serializer.errors)
