from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from event_manager.models import Event
from account_manager.models import UserProfile

from event_manager.api.serializers import EventSerializer

from drf_yasg.utils import swagger_auto_schema


@swagger_auto_schema(method='get')
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getEventsByLocation(request):
    query = request.query_params.get('q', '')
    events = Event.objects.filter(location=query)
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data)


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
    return Response(serializer)


