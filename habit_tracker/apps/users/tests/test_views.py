from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()

class UserViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
    
    def test_register_user(self):
        data = {
            'email': 'newuser@test.com',
            'password': 'newpass123'
        }
        response = self.client.post('/api/users/register/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_login_user(self):
        # Сначала создаем пользователя
        User.objects.create_user(
            email='login@test.com',
            password='login123'
        )
        
        data = {
            'email': 'login@test.com',
            'password': 'login123'
        }
        response = self.client.post('/api/users/login/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
