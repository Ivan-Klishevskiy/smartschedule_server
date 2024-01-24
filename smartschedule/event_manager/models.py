from django.db import models


class Event(models.Model):
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True, null=True)
    price = models.CharField(max_length=100, blank=True, null=True)
    image_url = models.URLField(max_length=200, blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    location = models.CharField(max_length=300, blank=True, null=True)
    source_url = models.URLField(max_length=200, blank=True, null=True)
    is_active = models.BooleanField(default=True)



    def __str__(self) -> str:
        return self.title