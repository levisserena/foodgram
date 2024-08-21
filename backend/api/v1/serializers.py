from django.db.transaction import atomic
from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import (ModelSerializer, ReadOnlyField,
                                        SerializerMethodField,
                                        SlugRelatedField)

from backend.settings import RECIPES_LIMIT
from recipes.models import (Favoritism, Ingredient, Recipe, RecipeIngredient,
                            RecipeTag, ShoppingCart, Tag)
from users.models import Follow, User


def is_authenticated_user(object_self):
    """Вернет кортеж request и бул значение аутентификация пользователя."""
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
            user=request.user, following=object).exists() else False


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
        extra_kwargs = {'email': {'required': True}}


class AvatarSerializer(ModelSerializer):
    """Сериализатор для добавления аватара."""

    avatar = Base64ImageField(required=True)

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
        source='ingredient_amount', many=True
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
            user=request.user, recipe=object.id).exists() else False

    def get_is_in_shopping_cart(self, object):
        """Обрабатывает поле is_in_shopping_cart."""
        request, result = is_authenticated_user(self)
        return True if result and ShoppingCart.objects.filter(
            user=request.user, recipe=object.id).exists() else False


class RecipeWriteSerializer(ModelSerializer):
    """Сериализатор модели рецептов, для запросов POST и PATCH."""

    tags = SlugRelatedField(
        slug_field='id', queryset=Tag.objects.all(), many=True, required=True
    )
    ingredients = IngredientWriteSerializer(many=True, required=True)
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

    @atomic
    def create(self, validated_data):
        """Обрабатывает создание нового рецепта."""
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        self.create_m2m_for_recipe(recipe, ingredients, tags)
        return recipe

    @atomic
    def update(self, instance, validated_data):
        """Обрабатывает изменение рецепта."""
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        RecipeIngredient.objects.filter(recipe=instance).delete()
        self.create_m2m_for_recipe(instance, ingredients, tags)
        return super().update(instance, validated_data)

    @staticmethod
    def create_m2m_for_recipe(recipe, ingredients, tags):
        """Создаст записи в связных таблицах для ингредиентов и тегов."""
        RecipeIngredient.objects.bulk_create([
            RecipeIngredient(
                recipe=recipe,
                ingredient=data['id'],
                amount=data['amount'],
            ) for data in ingredients
        ])
        recipe.tags.set([tag for tag in tags])

    def validate(self, attrs):
        """Проверит наличие полей tags и ingredients."""
        if 'tags' not in attrs:
            raise ValidationError('У рецепта должны быть тэги.')
        if 'ingredients' not in attrs:
            raise ValidationError('У рецепта должны быть ингредиенты.')
        return attrs

    def validate_image(self, image):
        """Проверит поле картинки у рецепта."""
        if not image:
            raise ValidationError('Строка не должна быть пустой.')
        return image

    def validate_ingredients(self, ingredients):
        """Проверит поле ингредиентов у рецепта."""
        list_id_ingredients = [ingredient['id'] for ingredient in ingredients]
        return self.check_ingredients_or_tags(
            ingredients, list_id_ingredients, 'Ингредиенты'
        )

    def validate_tags(self, tags):
        """Проверит поле тэгов у рецепта."""
        list_id_tags = [tag for tag in tags]
        return self.check_ingredients_or_tags(tags, list_id_tags, 'Тэги')

    def check_ingredients_or_tags(self, orders, list_id_order, message):
        """Для проверки наличия объектов и отсутствие их дублирования."""
        if not orders:
            raise ValidationError(f'У рецепта должны быть {message}.')
        if len(list_id_order) != len(set(list_id_order)):
            raise ValidationError(f'{message} не должны повторятся.')
        return orders


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


class UserSubscribeSerializer(ModelSerializer):
    """Сериализатор для модели подписки.

    Используется для создания и удаления подписок.
    """

    class Meta:
        """Метаданные."""

        model = Follow
        fields = ('user', 'following')

    def validate_following(self, value):
        """Проверит поле following."""
        if self.context['request'].user == value:
            raise ValidationError('Нельзя подписываться на самого себя.')
        return value

    def to_representation(self, instance):
        """После создания, вернет эти данные."""
        serializer = UserSubscriptionsSerializer(instance['following'])
        return serializer.data
