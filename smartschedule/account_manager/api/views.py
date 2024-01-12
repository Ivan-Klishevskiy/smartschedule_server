from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .serializers import UserProfileSerializer, RegisterSerializer, HobbySerializer
from account_manager.models import UserProfile, Hobby

from drf_yasg.utils import swagger_auto_schema

import geonamescache
from Levenshtein import distance
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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def citySearch(request):
    query = request.query_params.get('q', '')
    gc = geonamescache.GeonamesCache()
    cities = gc.search_cities(
        query, case_sensitive=False, contains_search=True)
    city_distances = [(city['name'], distance(
        query.lower(), city['name'].lower())) for city in cities]
    sorted_cities = sorted(city_distances, key=lambda x: x[1])
    city_names = [city[0] for city in sorted_cities[:10]]
    logger.info("Successfully", extra={
                'user': request.user, 'response_code': status.HTTP_200_OK})
    return Response(city_names)


@swagger_auto_schema(method='get')
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserProfile(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        return Response({'message': 'UserProfile not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = UserProfileSerializer(user_profile)
    logger.info("Successfully", extra={
                'user': request.user, 'response_code': status.HTTP_200_OK})
    return Response(serializer.data)


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
    hobbies = Hobby.objects.all()
    serializer = HobbySerializer(hobbies, many=True)
    logger.info("Successfully", extra={
                'user': request.user, 'response_code': status.HTTP_200_OK})
    return Response(serializer.data)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def updateUserProfile(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        serializer = UserProfileSerializer(user_profile, data=request.data, partial=True)
        
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            logger.info("Successfully updated user profile", extra={
                    'user': request.user.username, 'response_code': status.HTTP_200_OK})
            return Response(serializer.data)

    except UserProfile.DoesNotExist:
        logger.error('UserProfile not found', extra={
                'user': request.user.username, 'response_code': status.HTTP_404_NOT_FOUND})
        return Response({'message': 'UserProfile not found'}, status=status.HTTP_404_NOT_FOUND)

    except ValidationError as e:
        # ValidationError will be raised by is_valid() if raise_exception=True
        logger.error(f"Validation error: {e}", extra={
                'user': request.user.username, 'response_code': status.HTTP_400_BAD_REQUEST})
        return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        # Log other exceptions that might occur
        logger.error(f"Unexpected error: {str(e)}", extra={
                'user': request.user.username, 'response_code': status.HTTP_500_INTERNAL_SERVER_ERROR})
        return Response({'detail': 'An unexpected error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
    

    
