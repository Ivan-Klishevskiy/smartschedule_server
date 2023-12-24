from rest_framework.test import APITestCase
from account_manager.models import Hobby
from account_manager.api.serializers import HobbySerializer

from django.contrib.auth.models import User
from account_manager.models import UserProfile
from account_manager.api.serializers import UserProfileSerializer

from account_manager.api.serializers import RegisterSerializer

class HobbySerializerTestCase(APITestCase):
    def setUp(self):
        self.hobby_data = {'name': 'Painting', 'image_url': 'http://example.com/painting.jpg'}
        self.hobby = Hobby.objects.create(**self.hobby_data)

    def test_hobby_serializer(self):
        serializer = HobbySerializer(self.hobby)
        self.assertEqual(serializer.data, self.hobby_data)


class UserProfileSerializerTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.profile_data = {'age': 25, 'location': 'City', 'marital_status': 'Single', 'has_children': False}
        self.profile = UserProfile.objects.create(user=self.user, **self.profile_data)

    def test_user_profile_serializer(self):
        serializer = UserProfileSerializer(self.profile)
        data = serializer.data
        self.assertEqual(data['age'], self.profile_data['age'])
        self.assertEqual(data['location'], self.profile_data['location'])
        self.assertEqual(data['marital_status'], self.profile_data['marital_status'])
        self.assertEqual(data['has_children'], self.profile_data['has_children'])


class RegisterSerializerTestCase(APITestCase):
    def test_valid_register_serializer(self):
        valid_serializer_data = {
            'username': 'newuser',
            'email': 'user@example.com',
            'password': 'StrongPassword123'
        }
        serializer = RegisterSerializer(data=valid_serializer_data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_register_serializer(self):
        invalid_serializer_data = {
            'username': 'nu',
            'email': 'user@example',
            'password': 'weak'
        }
        serializer = RegisterSerializer(data=invalid_serializer_data)
        self.assertFalse(serializer.is_valid())


