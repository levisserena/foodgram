import base64
import re

from django.db.models import Q
from django.contrib.auth.models import AnonymousUser
from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import (BooleanField,
                                        CharField,
                                        CurrentUserDefault,
                                        EmailField,
                                        IntegerField,
                                        ImageField,
                                        ModelSerializer,
                                        ReadOnlyField,
                                        Serializer,
                                        SerializerMethodField,
                                        SlugField,
                                        SlugRelatedField)
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator

from backend.settings import (INVALID_USER_NAMES,
                              LENGTH_USERNAME,
                              PATTERN_USERNAME,
                              RECIPES_LIMIT)
from recipes.models import (Favoritism,
                            Ingredient,
                            Recipe,
                            RecipeIngredient,
                            RecipeTag,
                            ShopingCart,
                            Tag)
from users.models import User, Follow
from .paginations import RecipeForSubscriptionsPagination


class Base64ImageField(ImageField):
    """Определяет поле, для декодирования строки Base64."""

    def to_internal_value(self, data):
        """Проверка данных на соответствие."""
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


def is_authenticated_user(object_self):
    """Вернет кортеж request и бул значение аунтификации пользователя."""
    request = object_self.context.get('request', None)
    return (request, request and request.user.is_authenticated)


class UserFoodgramSerializer(UserSerializer):
    """Сериализатор для модели пользователей.

    Используется Djoser.
    """

    is_subscribed = SerializerMethodField()

    class Meta:
        """Метаданные."""

        model = User
        fields = (
            'id', 'email', 'username', 'first_name',
            'last_name', 'avatar', 'is_subscribed',
        )
        read_only_fields = ('id', 'avatar', 'is_subscribed')

    def get_is_subscribed(self, object):
        """Обрабатывает поле is_subscribed."""
        request, result = is_authenticated_user(self)
        return True if result and Follow.objects.filter(
            user=request.user, following=object) else False


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

    def validate_username(self, username):
        """Не допускает имя пользователя me и проверяет по паттерну."""
        if not re.match(PATTERN_USERNAME, username):
            raise ValidationError('В имене используется неразрешенные знаки.')
        if username in INVALID_ESER_NAMES:
            raise ValidationError('Это имя не допустимо.')
        return username


class AvatarSerializer(ModelSerializer):
    """Сериализатор для добавления аватара."""

    avatar = Base64ImageField(required=True)  # allow_null=True

    class Meta:
        """Метаданные."""

        model = User
        fields = ('avatar',)


class IngredientSerializer(ModelSerializer):
    """Сериализатор модели ингредиентов."""

    class Meta:
        """Метаданные."""

        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')
        read_only_fields = ('id', 'name', 'measurement_unit')


class TagSerializer(ModelSerializer):
    """Сериализатор модели тэгов."""

    class Meta:
        """Метаданные."""

        model = Tag
        fields = ('id', 'name', 'slug')
        read_only_fields = ('id', 'name', 'slug')


class IngredientReadSerializer(ModelSerializer):
    """Сериализатор модели ингредиентов."""

    id = ReadOnlyField(source='ingredient.id')
    name = ReadOnlyField(source='ingredient.name')
    measurement_unit = ReadOnlyField(source='ingredient.measurement_unit')

    class Meta:
        """Метаданные."""

        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class IngredientWriteSerializer(ModelSerializer):
    """Сериализатор модели ингредиентов."""

    id = SlugRelatedField(
        slug_field='id',
        queryset=Ingredient.objects.all(),
    )

    class Meta:
        """Метаданные."""

        model = RecipeIngredient
        fields = ('id', 'amount')


class RecipeReadSerializer(ModelSerializer):
    """Сериализатор модели рецептов, для запросов GET."""

    author = UserFoodgramSerializer()
    tags = TagSerializer(many=True)
    ingredients = IngredientReadSerializer(
        source='ingridient_amount', many=True
    )
    is_favorited = SerializerMethodField()
    is_in_shopping_cart = SerializerMethodField()

    class Meta:
        """Метаданные."""

        model = Recipe
        fields = (
            'id', 'name', 'tags', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'image', 'text', 'cooking_time',
        )
        read_only_fields = (
            'id', 'is_subscribed', 'is_in_shopping_cart', 'author'
        )

    def get_is_favorited(self, object):
        """Обрабатывает поле is_favorited."""
        request, result = is_authenticated_user(self)
        return True if result and Favoritism.objects.filter(
            user=request.user, recipe=object.id) else False

    def get_is_in_shopping_cart(self, object):
        """Обрабатывает поле is_in_shopping_cart."""
        request, result = is_authenticated_user(self)
        return True if result and ShopingCart.objects.filter(
            user=request.user, recipe=object.id) else False


class RecipeWriteSerializer(ModelSerializer):
    """Сериализатор модели рецептов, для запросов POST и PATCH."""

    tags = SlugRelatedField(
        slug_field='id', queryset=Tag.objects.all(), many=True
    )
    ingredients = IngredientWriteSerializer(
        many=True
    )
    image = Base64ImageField(required=True)

    class Meta:
        """Метаданные."""

        model = Recipe
        fields = (
            'name', 'tags', 'ingredients', 'image', 'text', 'cooking_time',
        )

    def to_representation(self, instance):
        """После создания, вернет эти данные."""
        serializer = RecipeReadSerializer(instance)
        return serializer.data

    def create(self, validated_data):
        """Обрабатывает создание нового рецепта."""
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        RecipeTag.objects.bulk_create([
            RecipeTag(recipe=recipe, tag=tag) for tag in tags
        ])
        RecipeIngredient.objects.bulk_create([
            RecipeIngredient(
                recipe=recipe, amount=data['amount'], ingredient=data['id']
            ) for data in ingredients
        ])
        return recipe

    def update(self, instance, validated_data):
        """Обрабатывает изменение рецепта."""
        instance.image = validated_data.get('image', instance.image)
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time
        )
        if 'ingredients' in validated_data:
            ingredients_data = validated_data.pop('ingredients')
            RecipeIngredient.objects.filter(recipe=instance).delete()
            RecipeIngredient.objects.bulk_create([
                RecipeIngredient(
                    recipe=instance,
                    ingredient=data['id'],
                    amount=data['amount'],
                ) for data in ingredients_data
            ])
        if 'tags' in validated_data:
            tags_data = validated_data.pop('tags')
            instance.tags.set([tag for tag in tags_data])
        instance.save()
        return instance


class RecipeShortSerializer(ModelSerializer):
    """Сериализатор модели рецептов.

    Используется для отображения рецептов у подписанных пользователей и
    избранного.
    """

    class Meta:
        """Метаданные."""

        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('id', 'name', 'image', 'cooking_time')


class UserSubscriptionsSerializer(UserFoodgramSerializer):
    """Сериализатор для модели пользователей.

    Используется для просмотра на кого подписан пользователь.
    """

    recipes = SerializerMethodField()
    recipes_count = SerializerMethodField()

    class Meta:
        """Метаданные."""

        model = User
        fields = (
            'id', 'email', 'username', 'first_name',
            'last_name', 'avatar', 'is_subscribed',
            'recipes', 'recipes_count',
        )
        read_only_fields = (
            'id', 'avatar', 'is_subscribed', 'recipes', 'recipes_count',
        )

    def get_recipes(self, object):
        """Обрабатывает поле "рецепты"."""
        request = self.context.get('request', None)
        recipes_limit = RECIPES_LIMIT if not request else int(request.GET.get(
            'recipes_limit', RECIPES_LIMIT
        ))
        instance = Recipe.objects.filter(author=object.id)[:recipes_limit]
        serializer = RecipeShortSerializer(
            instance=instance, many=True,
        )
        return serializer.data

    def get_recipes_count(self, object):
        """Обрабатывает поле "счетчик рецептов"."""
        return Recipe.objects.filter(author=object.id).count()


# class UsedSubscribeSerializer(ModelSerializer):
#     """Сериализатор для модели подписки."""

#     user = SlugRelatedField(
#         slug_field='username', read_only=True, default=CurrentUserDefault(),
#     )
#     following = SlugRelatedField(
#         slug_field='username', queryset=User.objects.all(),
#     )

#     class Meta:
#         """Метаданные."""

#         model = Follow
#         fields = ('user', 'following')
#         read_only_fields = ('user', 'following')
#         validators = (
#             UniqueTogetherValidator(
#                 queryset=Follow.objects.all(),
#                 fields=('user', 'following'),
#                 message='На этого пользователя Вы уже подписаны!'
#             ),
#         )

#     def validate_following(self, following):
#         """Валидирует поле following.

#         Подписываться на самого себя нельзя.
#         """
#         user = self.context['request'].user
#         if user == following:
#             raise ValidationError(detail='Подписаться на самого себя нельзя.')
#         return following

#     def to_representation(self, instance):
#         """После создания, вернет эти данные."""
#         serializer = UserSubscriptionsSerializer(instance)
#         return serializer.data
