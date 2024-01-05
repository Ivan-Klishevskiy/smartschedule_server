from django.urls import path
from . import views


urlpatterns = [
    path('by-fields', view=views.getEventByField, name='events_by_fields'),
    path('by-user', view=views.getEventsByUser, name='events_by_user'),
]