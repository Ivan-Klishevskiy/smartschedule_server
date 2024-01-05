from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from account_manager.models import UserProfile


class AccountManagerTestCase(APITestCase):
    fixtures = ['event_initial_data.json']

    def setUp(self):
        super(AccountManagerTestCase, self).setUp()
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

    def test_get_events_by_fields(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_token_for_user())
        url = reverse('events_by_fields')
        data = {
            'title':'Tech Conference',
            'location': 'Convention Center',

        }
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIsInstance(response.data, list)

        self.assertTrue(
            any(item['title'] ==
                'Tech Conference' for item in response.data),
            "Tech Conference not found in response"
        )

        self.assertTrue(
            any(item['location'] ==
                'Convention Center' for item in response.data),
            "Convention Center not found in response"
        )

    def test_get_events_by_date(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_token_for_user())
        url = reverse('events_by_fields')
        data = {
            'start_date':'2024-03-05T09:00:00Z',
            "end_date": "2024-03-06T18:00:00Z",

        }
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIsInstance(response.data, list)

        self.assertTrue(
            any(item['start_date'] ==
                '2024-03-05T09:00:00Z' for item in response.data),
            "Convention Center not found in response"
        )

        self.assertTrue(
            any(item['end_date'] ==
                '2024-03-06T18:00:00Z' for item in response.data),
            "Convention Center not found in response"
        )

        