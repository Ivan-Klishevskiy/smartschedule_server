from datetime import datetime
import re
from django.forms import ValidationError
from rest_framework import serializers
from account_manager.models import UserProfile, Hobby
from django.contrib.auth.models import User
from django.core.validators import validate_email

from event_manager.api.serializers import EventSerializer
from event_manager.models import Event


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

    birthday_date = serializers.DateField(
        allow_null=True,
        required=False,
        format='%Y-%m-%d',
        input_formats=['%Y-%m-%d', 'iso-8601']
    )

    events = serializers.PrimaryKeyRelatedField(
        many=True, 
        queryset=Event.objects.all(), 
        required=False
    )

    class Meta:
        model = UserProfile
        fields = ['user', 'birthday_date', 'location', 'hobbies',
                  'marital_status', 'has_children','events']

    def validate_birth_date(self, value):
            if value is not None:
                try:
                    datetime.strptime(str(value), '%Y-%m-%d')
                except ValueError:
                    raise serializers.ValidationError(
                        "birthday_date must be in YYYY-MM-DD format")

            return value

    def update(self, instance, validated_data):
        hobbies = validated_data.pop('hobbies', None)
        events = validated_data.pop('events', None)
        
        if hobbies is not None:
            instance.hobbies.set(hobbies)

        if events is not None:
            instance.events.set(events)

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
