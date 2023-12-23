import re
from django.forms import ValidationError
from rest_framework import serializers
from account_manager.models import UserProfile, Hobby
from django.contrib.auth.models import User
from django.core.validators import validate_email


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
        fields = ['user', 'age', 'location', 'hobbies',
                  'marital_status', 'has_children']

    def update(self, instance, validated_data):

        hobbies = validated_data.pop('hobbies', None)
        if hobbies is not None:
            instance.hobbies.set(hobbies)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class RegisterSerializer(serializers.ModelSerializer):

    def validate_email(self, value):
        try:
            validate_email(value)
        except ValidationError as e:
            raise serializers.ValidationError("Invalid email address.")
        return value

    def validate_username(self, value):
        # Check for minimum username length
        if len(value) < 5:
            raise serializers.ValidationError(
                "The username must be at least 5 characters long.")

        # Check for the presence of at least one letter
        if not re.search("[a-zA-Z]", value):
            raise serializers.ValidationError(
                "The username must contain at least one Latin letter.")

        # Check for the use of only Latin letters and digits
        if not re.fullmatch("[A-Za-z0-9]+", value):
            raise serializers.ValidationError(
                "The username can only contain Latin letters and digits.")

        return value

    def validate_password(self, value):
        # Check for minimum password length
        if len(value) < 8:
            raise serializers.ValidationError(
                "The password must be at least 8 characters long.")

        # Check for at least one letter
        if not re.search("[a-zA-Z]", value):
            raise serializers.ValidationError(
                "The password must contain at least one letter.")

        # Check for at least one digit
        if not re.search("[0-9]", value):
            raise serializers.ValidationError(
                "The password must contain at least one digit.")

        # Check for the use of only Latin letters, digits and underscores
        if not re.fullmatch("[A-Za-z0-9_]+", value):
            raise serializers.ValidationError(
                "The password can only contain Latin letters, digits, and underscores.")

        return value


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
