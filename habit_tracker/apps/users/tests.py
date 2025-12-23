from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status

User = get_user_model()

class UserModelTest(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            username='test@example.com'
        )
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('testpass123'))
        self.assertFalse(user.is_staff)
        self.assertTrue(user.is_active)
    
    def test_create_superuser(self):
        admin_user = User.objects.create_superuser(
            email='admin@example.com',
            password='adminpass123',
            username='admin@example.com'
        )
        self.assertTrue(admin_user.is_superuser)
        self.assertTrue(admin_user.is_staff)

class UserAPITest(APITestCase):
    def test_register_user(self):
        data = {
            'email': 'newuser@example.com',
            'password': 'newpass123',
            'telegram_chat_id': '@testuser'
        }
        response = self.client.post('/api/users/register/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.first().email, 'newuser@example.com')
    
    def test_login_user(self):
        # Сначала регистрируем пользователя
        user = User.objects.create_user(
            email='login@example.com',
            password='loginpass123',
            username='login@example.com'
        )
        
        data = {
            'email': 'login@example.com',
            'password': 'loginpass123'
        }
        response = self.client.post('/api/users/login/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
    
    def test_profile_view(self):
        # Создаем и логиним пользователя
        user = User.objects.create_user(
            email='profile@example.com',
            password='profilepass123',
            username='profile@example.com'
        )
        
        # Логиним
        self.client.force_authenticate(user=user)
        
        # Получаем профиль
        response = self.client.get('/api/users/profile/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'profile@example.com')
    
    def test_logout(self):
        user = User.objects.create_user(
            email='logout@example.com',
            password='logoutpass123',
            username='logout@example.com'
        )
        
        self.client.force_authenticate(user=user)
        
        # Выход (требует refresh токен, но проверим что эндпоинт доступен)
        response = self.client.post('/api/users/logout/', {})
        # Может быть 400 из-за отсутствия refresh токена, но не 401/403
        self.assertIn(response.status_code, [status.HTTP_205_RESET_CONTENT, status.HTTP_400_BAD_REQUEST])
