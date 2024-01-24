from django.http import JsonResponse
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


from data_processing.event_generation.scrapers.goout_scraper import collect_script_contents_gout

from .serializers import UserProfileSerializer, RegisterSerializer, HobbySerializer
from account_manager.models import UserProfile, Hobby

from ..services import account_services

from drf_yasg.utils import swagger_auto_schema


import logging

logger = logging.getLogger('api_log')


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = user.username
        logger.info("Successfully", extra={
                    'response_code': status.HTTP_200_OK})
        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@swagger_auto_schema(method='get')
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def searchLocation(request):
    query = request.query_params.get('q', '')

    cache_key = f'locations_{query}'
    cached_locations = cache.get(cache_key)
    if cached_locations is not None:
        return Response(cached_locations)
    
    
    locations = account_services.get_list_location_by_query(query)

    cache.set(cache_key, locations, timeout=300)

    logger.info("Successfully", extra={
                'user': request.user, 'response_code': status.HTTP_200_OK})
    return Response(locations)


@swagger_auto_schema(method='get')
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserProfile(request):

    user_profile = account_services.get_user_profile(user=request.user)

    if user_profile:
        serializer = UserProfileSerializer(user_profile)
        logger.info("Successfully", extra={
                    'user': request.user, 'response_code': status.HTTP_200_OK})
        return Response(serializer.data)
    else:
        logger.info('UserProfile not found', extra={
                    'user': request.user, 'response_code': status.HTTP_404_NOT_FOUND})
        return Response({'message': 'UserProfile not found'}, status=status.HTTP_404_NOT_FOUND)


@swagger_auto_schema(method='post', request_body=RegisterSerializer)
@api_view(['POST'])
@permission_classes([])
def registerUser(request):
    serializer = RegisterSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        logger.info("Successfully registered", extra={
            'user': request.user, 'response_code': status.HTTP_200_OK})
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        logger.info("Unregistered", extra={
                    'response_code': status.HTTP_400_BAD_REQUEST})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='get')
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listHobbies(request):
    hobbies_query_set = account_services.get_all_hobby()

    paginator = PageNumberPagination()
    paginated_hobbies = paginator.paginate_queryset(hobbies_query_set, request)

    if paginated_hobbies is not None:
        serializer = HobbySerializer(paginated_hobbies, many=True)
        return paginator.get_paginated_response(serializer.data)

    logger.error('No hobbies found', extra={
        'user': request.user.username, 'response_code': status.HTTP_404_NOT_FOUND})
    return Response({'message': 'No hobbies found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def updateUserProfile(request):
    user_profile = account_services.get_user_profile(user=request.user)

    if user_profile is None:
        logger.error('UserProfile not found', extra={
            'user': request.user.username, 'response_code': status.HTTP_404_NOT_FOUND})
        return Response({'message': 'UserProfile not found'}, status=status.HTTP_404_NOT_FOUND)

    try:
        serializer = UserProfileSerializer(
            user_profile, data=request.data, partial=True)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            logger.info("Successfully updated user profile", extra={
                'user': request.user.username, 'response_code': status.HTTP_200_OK})
            return Response(serializer.data)

    except ValidationError as e:
        logger.error(f"Validation error: {e}", extra={
            'user': request.user.username, 'response_code': status.HTTP_400_BAD_REQUEST})
        return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", extra={
            'user': request.user.username, 'response_code': status.HTTP_500_INTERNAL_SERVER_ERROR})
        return Response({'detail': 'An unexpected error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])  # TODO delete this method (just for develop)
def scraper(request):
    collect_script_contents_gout()
    return Response('OK')
