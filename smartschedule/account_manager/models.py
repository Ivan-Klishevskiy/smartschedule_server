from django.db import models
from django.contrib.auth.models import User
from event_manager.models import Event


class Hobby(models.Model):
    name = models.CharField(max_length=100)
    image_url = models.URLField(max_length=200)

    def __str__(self):
        return self.name
    

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', null=True)
    birthday_date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=100, blank=True)
    hobbies = models.ManyToManyField(Hobby, blank=True)
    marital_status = models.CharField(max_length=100, blank=True)
    has_children = models.BooleanField(default=False)

    events = models.ManyToManyField(Event, related_name='profiles')

    def __str__(self):
        return self.user.username
    