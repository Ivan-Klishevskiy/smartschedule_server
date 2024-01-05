from rest_framework import serializers
from event_manager.models import Event


class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = [
            'id',
            'title',
            'image_url',
            'start_date',
            'end_date',
            'location',
            'source_url'
        ]
