from django.urls import path, re_path

from . import views
from .views import MyTokenObtainPairView, listHobbies, updateUserProfile, searchLocation, scraper

from rest_framework_simplejwt.views import (TokenRefreshView,)


urlpatterns = [
    re_path(r'^user_profile/?$', views.getUserProfile, name='user_profile'),

    re_path(r'^token/?$', MyTokenObtainPairView.as_view(),
            name='token_obtain_pair'),

    re_path(r'^token/refresh/?$', TokenRefreshView.as_view(),
            name='token_refresh'),

    re_path(r'^register/?$', views.registerUser, name='register'),

    re_path(r'^user-profile/update/?$', updateUserProfile,
            name='update_user_profile'),

    re_path(r'^hobbies/?$', listHobbies, name='list_hobbies'),

    re_path(r'^location-search/?$', searchLocation, name='location_search'),

    re_path(r'^scraper/?$', scraper, name='scraper'),

]
