from rest_framework import serializers
from account_manager.models import UserProfile, Hobby
from django.contrib.auth.models import User


class HobbySerializer(serializers.ModelSerializer):
    class Meta:
        model = Hobby
        fields = ['name', 'image_url']


class UserProfileSerializer(serializers.ModelSerializer):
    hobbies = serializers.SlugRelatedField(
        many=True,
        queryset=Hobby.objects.all(),
        slug_field='name',
        required=False
    )

    class Meta:
        model = UserProfile
        fields = ['user', 'age', 'location', 'hobbies', 'marital_status', 'has_children']

    def update(self, instance, validated_data):
        # Обновление хобби пользователя
        hobbies = validated_data.pop('hobbies', None)
        if hobbies is not None:
            instance.hobbies.set(hobbies)

        # Обновление других полей
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class RegisterSerializer(serializers.ModelSerializer):

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

        UserProfile.objects.create(user=user)

        return user