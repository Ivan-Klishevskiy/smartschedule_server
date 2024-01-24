from event_manager.services import event_services
from event_manager.api.serializers import EventSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema


import logging

logger = logging.getLogger(__name__)


@swagger_auto_schema(method='get')
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getEventsByUser(request):
    events_query_set = event_services.get_events_by_user(request.user)

    paginator = PageNumberPagination()
    paginated_events = paginator.paginate_queryset(events_query_set, request)

    if paginated_events is not None:
        serializer = EventSerializer(paginated_events, many=True)
        return paginator.get_paginated_response(serializer.data)

    logger.error('UserProfile not found', extra={
        'response_code': status.HTTP_404_NOT_FOUND})
    return Response({'message': 'No events found'}, status=status.HTTP_404_NOT_FOUND)


@swagger_auto_schema(method='get')
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getEventByField(request):
    title_str = request.GET.get('title', '')
    description_str = request.GET.get('description', '')
    location_str = request.GET.get('location', '')
    start_date_str = request.GET.get('start_date', '')
    end_date_str = request.GET.get('end_date', '')
    is_active_str = request.GET.get('is_active', 'true')

    try:
        events_query_set = event_services.filter_events(
            title_str, description_str, location_str, start_date_str, end_date_str, is_active_str
        )

        paginator = PageNumberPagination()
        paginated_events = paginator.paginate_queryset(
            events_query_set, request)

        if paginated_events is not None:
            serializer = EventSerializer(paginated_events, many=True)
            return paginator.get_paginated_response(serializer.data)

        return Response({'message': 'No events found'}, status=status.HTTP_404_NOT_FOUND)

    except NotFound:
        return Response({'message': 'Page not found'}, status=status.HTTP_404_NOT_FOUND)
    except ValueError as e:
        logger.error(f"Invalid date format: {str(e)}", extra={
                     'user': request.user.username, 'response_code': status.HTTP_400_BAD_REQUEST})
        return Response("Invalid date format. Please use the ISO 8601 format (YYYY-MM-DDTHH:MM).",
                        status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.error(f"Error in getEventByField: {str(e)}", extra={
                     'user': request.user.username, 'response_code': status.HTTP_500_INTERNAL_SERVER_ERROR})
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
