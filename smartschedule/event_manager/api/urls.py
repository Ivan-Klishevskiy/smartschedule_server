from django.urls import path, re_path
from . import views


urlpatterns = [
    re_path(r'^by-fields/?$', view=views.getEventByField, name='events_by_fields'),
    re_path(r'^by-user/?$', view=views.getEventsByUser, name='events_by_user'),
]