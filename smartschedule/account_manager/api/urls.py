from django.urls import path
from . import views
from .views import MyTokenObtainPairView, listHobbies, updateUserProfile

from rest_framework_simplejwt.views import (
   
    TokenRefreshView,
)

urlpatterns = [
    path('', views.getRoutes),

    path('user_profile/', views.getUserProfile, name='user_profile'),
    

    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.registerUser, name='register'),
    path('user-profile/update/', updateUserProfile, name='update_user_profile'),

    path('hobbies/', listHobbies, name='list_hobbies'),
]