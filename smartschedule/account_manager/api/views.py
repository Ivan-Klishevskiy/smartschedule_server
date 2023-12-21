from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .serializers import UserProfileSerializer, RegisterSerializer
from account_manager.models import UserProfile

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = user.username
        

        return token
    
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/api/token',
        '/api/token/refresh',
    ]

    return Response(routes)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserProfile(request):
    user_profile = UserProfile.objects.all()
    serializer = UserProfileSerializer(user_profile, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([])
def registerUser(request):
    serializer = RegisterSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)