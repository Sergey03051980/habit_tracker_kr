from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from habit_tracker.apps.habits.models import Habit

User = get_user_model()

class HabitViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='viewtest@test.com',
            password='test123'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        
        # Создаем тестовую привычку
        self.habit = Habit.objects.create(
            user=self.user,
            name='Тест привычка',
            duration=60
        )
    
    def test_list_habits(self):
        response = self.client.get('/api/habits/habits/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_habit(self):
        data = {
            'name': 'Новая привычка',
            'duration': 45,
            'reward': 'Вознаграждение'
        }
        response = self.client.post('/api/habits/habits/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
