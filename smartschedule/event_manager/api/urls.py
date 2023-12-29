from django.urls import path
from . import views


urlpatterns = [
    path('by-location', view=views.getEventsByLocation, name='events_by_location'),
    path('by-user', view=views.getEventsByLocation, name='events_by_user'),
]