from django.contrib import admin
from django.urls import path, include
from .yasg import urlpatterns as doc_urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/account/', include('account_manager.api.urls')),
    path('api/events/', include('event_manager.api.urls'))
]

urlpatterns += doc_urls
