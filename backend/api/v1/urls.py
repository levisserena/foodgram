from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import avatar


urlpatterns = [
    path('users/me/avatar/', avatar, name='avatar'),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include('djoser.urls')),
]
