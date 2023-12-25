from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from account_manager.models import UserProfile


class AccountManagerTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', email='test@example.com', password='testpassword1')
        UserProfile.objects.create(user=self.user)

    def get_token_for_user(self):
        url = reverse('token_obtain_pair')
        data = {
            'username': 'testuser',
            'password': 'testpassword1'
        }
        response = self.client.post(url, data)
        return response.data['access']

    def test_register_user(self):
        url = reverse('register')
        data = {
            'username': 'newuser',
            'email': 'usernew@example.com',
            'password': 'newpassword123'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)

    def test_get_user_profile(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_token_for_user())
        url = reverse('user_profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_user_profile(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_token_for_user())
        url = reverse('update_user_profile')
        data = {'age': 18}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.profile.age, 18)

    def test_list_hobbies(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_token_for_user())
        url = reverse('list_hobbies')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)

    def test_token_refresh(self):
        url = reverse('token_obtain_pair')
        data = {
            'username': 'testuser',
            'password': 'testpassword1'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        refresh_token = response.data['refresh']

        refresh_url = reverse('token_refresh')
        refresh_data = {
            'refresh': refresh_token
        }
        refresh_response = self.client.post(refresh_url, refresh_data)
        self.assertEqual(refresh_response.status_code, status.HTTP_200_OK)
        self.assertIn('access', refresh_response.data)

    def test_city_search(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_token_for_user())
        url = reverse('city_search')
        response = self.client.get(url, {'q': 'Tel Aviv'})
        print(response.data)
        self.assertIn('Tel Aviv', response.data)

        response = self.client.get(url, {'q': 'Minsk'})
        print(response.data)
        self.assertIn('Minsk', response.data)

        response = self.client.get(url, {'q': 'New York'})
        print(response.data)
        self.assertIn('New York City', response.data)
