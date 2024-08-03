import base64
import re

from django.db.models import Q
from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import (BooleanField,
                                        CharField,
                                        EmailField,
                                        IntegerField,
                                        ImageField,
                                        ModelSerializer,
                                        Serializer,
                                        SerializerMethodField,
                                        SlugField,
                                        SlugRelatedField)
from rest_framework.validators import UniqueValidator

from backend.settings import (INVALID_ESER_NAMES,
                              LENGTH_USERNAME,
                              PATTERN_USERNAME)
from users.models import User, Follow


class Base64ImageField(ImageField):
    """Определяет поле, для декодирования строки Base64."""

    def to_internal_value(self, data):
        """Проверка данных на соответствие."""
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class UserFoodgramSerializer(UserSerializer):
    """Сериализатор для модели пользователей.

    Используется Djoser.
    """

    username = CharField(max_length=LENGTH_USERNAME, required=True)
    is_subscribed = SerializerMethodField()

    class Meta:
        """Метаданные."""

        model = User
        fields = (
            'id', 'email', 'username', 'first_name', 'last_name', 'avatar',
            'is_subscribed',
        )
        read_only_fields = ('id', 'avatar', 'is_subscribed')

    def validate_username(self, username):
        """Не допускает имя пользователя me."""
        if not re.match(PATTERN_USERNAME, username):
            raise ValidationError('В имене используется неразрешенные знаки.')
        if username in INVALID_ESER_NAMES:
            raise ValidationError('Это имя не допустимо.')
        return username

    # def validate(self, data):
    #     """Валидирует поля username и email.

    #     У пользователя не должно быть возможности использовать один e-mail
    #     разными пользователями.
    #     """
    #     username = (data.get('username', None)
    #                 or self.context['request'].user.username)
    #     email = (data.get('email', None)
    #              or self.context['request'].user.email)
    #     if User.objects.filter(
    #         Q(email__iexact=email) & ~Q(username__iexact=username)
    #         | Q(username__iexact=username) & ~Q(email__iexact=email)
    #     ):
    #         raise ValidationError(
    #             detail='Неверная пара имени пользователя и e-mail.'
    #         )
    #     return data

    def get_is_subscribed(self, object):
        """Обрабатывает поле is_subscribed."""
        return True if Follow.objects.filter(
            user=self.context['request'].user, following=object
        ) else False


class UserCreateFoodgramSerializer(UserCreateSerializer):
    """Сериализатор для создания объекта модели пользователей.

    Используется Djoser.
    """

    class Meta:
        """Метаданные."""

        model = User
        fields = (
            'id', 'email', 'username', 'first_name', 'last_name', 'password',
        )
        read_only_fields = ('id',)
        write_only_fields = ('password',)
        extra_kwargs = {
            'email': {'required': True},
            'username': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'password': {'required': True},
        }


class AvatarSerializer(ModelSerializer):
    """Сериализатор для добавления аватара."""

    avatar = Base64ImageField(required=True)  # allow_null=True

    class Meta:
        """Метаданные."""

        model = User
        fields = ('avatar',)
