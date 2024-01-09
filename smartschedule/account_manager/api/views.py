from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

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


@swagger_auto_schema(method='patch', request_body=UserProfileSerializer)
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def updateUserProfile(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        logger.info('UserProfile not found', extra={
                'user': request.user, 'response_code': status.HTTP_404_NOT_FOUND})
        return Response({'message': 'UserProfile not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = UserProfileSerializer(
        user_profile, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        logger.info("Successfully", extra={
                'user': request.user, 'response_code': status.HTTP_200_OK})
        return Response(serializer.data)
    
    logger.info(serializer.errors, extra={
                'user': request.user, 'response_code': status.HTTP_400_BAD_REQUEST})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
