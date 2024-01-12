from rest_framework import serializers
from event_manager.models import Event
from datetime import datetime

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

    def validate_start_date(self, value):
        try:
            datetime.strptime(value, '%Y-%m-%dT%H:%M')
        except ValueError:
            raise serializers.ValidationError("start_date must be in YYYY-MM-DDTHH:MM format")
        
        return value
    
    def validate_end_date(self, value):
        try:
            datetime.strptime(value, '%Y-%m-%dT%H:%M')
        except ValueError:
            raise serializers.ValidationError("start_date must be in YYYY-MM-DDTHH:MM format")
        
        return value
