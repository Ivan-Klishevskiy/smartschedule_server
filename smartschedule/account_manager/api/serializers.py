from rest_framework import serializers
from account_manager.models import UserProfile
from django.contrib.auth.models import User

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class RegisterSerializer(serializers.ModelSerializer):
    # password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def save(self):
        user = User(
            email=self.validated_data['email'],
            username=self.validated_data['username']
        )
        password = self.validated_data['password']

        user.set_password(password)
        user.save()

        UserProfile.objects.create(user=user, body="")

        return user