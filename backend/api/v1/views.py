import os

from django.contrib.auth.tokens import default_token_generator
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import RetrieveAPIView, UpdateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework_simplejwt.tokens import AccessToken

from users.models import User
from .serializer import AvatarSerializer
from .utilities import delete_image


@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def avatar(request):
    """Добавляет или удаляет аватар пользователя."""
    instance = get_object_or_404(User, pk=request.user.pk)
    path = str(instance.avatar)
    if request.method == 'DELETE':
        delete_image(path)
        instance.avatar = None
        instance.save()
        return Response({}, status=status.HTTP_204_NO_CONTENT)
    serializer = AvatarSerializer(instance=instance, data=request.data)
    serializer.is_valid(raise_exception=True)
    delete_image(path)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)
