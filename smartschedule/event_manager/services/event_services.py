import logging

from event_manager.models import Event
from account_manager.models import UserProfile
from event_manager.api.serializers import EventSerializer
from dateutil import parser
from django.db.models import Q

logger = logging.getLogger('api_log')


def filter_events(title, description, location, start_date, end_date, is_active):
    query = Q()
    try:
        if title:
            query &= Q(title__icontains=title)
        if description:
            query &= Q(description__icontains=description)
        if location:
            query &= Q(location__icontains=location)
        if start_date:
            parse_start_date = parser.isoparse(start_date).date()
            query &= Q(start_date__date=parse_start_date)
        if end_date:
            parse_end_date = parser.isoparse(end_date).date()
            query &= Q(end_date__date=parse_end_date)
        query &= Q(is_active=is_active.lower() in ['true', '1'])

        events = Event.objects.filter(query)
        return events
    except Exception as e:
        raise


def get_events_by_user(user):
    try:
        user_profile = UserProfile.objects.get(user=user)
        events = user_profile.events.all()
        return events
    except UserProfile.DoesNotExist:
        return None
