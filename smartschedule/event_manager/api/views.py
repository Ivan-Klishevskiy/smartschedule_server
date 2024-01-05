from django.http import JsonResponse
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from event_manager.models import Event
from account_manager.models import UserProfile
from dateutil import parser

from event_manager.api.serializers import EventSerializer

from drf_yasg.utils import swagger_auto_schema



@swagger_auto_schema(method='get')
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getEventsByUser(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        return Response({'message': 'UserProfile not found'}, status=status.HTTP_404_NOT_FOUND)
    events = user_profile.events.all()
    serializer = EventSerializer(events, many=True)
    return Response(serializer, status=status.HTTP_200_OK)


@swagger_auto_schema(method='get')
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getEventByField(request):
    
    title_str = request.GET.get('title', '')
    location_str =request.GET.get('location', '')
    start_date_str = request.GET.get('start_date', '')
    end_date_str = request.GET.get('end_date', '')
    is_active_str = request.GET.get('is_active', 'true')

    query = Q()

    if title_str:
        query &= Q(title__icontains=title_str) 

    if location_str:
        query &= Q(location__icontains=location_str)

    if start_date_str:
        try:
            parse_start_date = parser.isoparse(start_date_str).date()
            query &= Q(start_date__date=parse_start_date)
        except ValueError:
            return Response("Invalid date format. Please use the ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ).",
                             status=status.HTTP_400_BAD_REQUEST)
        
    if end_date_str:
        try:
            parse_end_date = parser.isoparse(end_date_str).date()
            query &= Q(end_date__date=parse_end_date)
        except ValueError:
            return Response("Invalid date format. Please use the ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ).",
                             status=status.HTTP_400_BAD_REQUEST)
        
    query &= Q(is_active=is_active_str.lower() in ['true', 'True', '1'])
    

    events = Event.objects.filter(query)
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
    

    
    


