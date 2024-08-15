from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from djoser.views import UserViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action, api_view
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from backend.settings import DOMAIN_NAME, HTTPS, LOCALLY
from recipes.models import (Favoritism, Ingredient, Recipe, RecipeIngredient,
                            ShoppingCart, ShortLink, Tag)
from users.models import Follow, User
from .permission import IsAdminOrAuthor
from .filters import IngredientSearchFilter, RecipeFilterSet
from .serializers import (AvatarSerializer, IngredientSerializer,
                          RecipeReadSerializer, RecipeShortSerializer,
                          RecipeWriteSerializer, TagSerializer,
                          UserSubscriptionsSerializer)


def delete_or_400(object, message):
    """Возвращает ошибку 400 если объекта нет, или удалит его."""
    if not object.exists():
        return Response({'errors': f'{message}'},
                        status=status.HTTP_400_BAD_REQUEST)
    object.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


def exists_then_400(message):
    """Возвращает ошибку 400 с сообщением, что объект уже есть."""
    return Response({'errors': f'{message}'},
                    status=status.HTTP_400_BAD_REQUEST)


class UserFoodgramViewSet(UserViewSet):
    """Представление, обрабатывающее запросы к модели пользователь."""

    def get_permissions(self):
        """Переопределяет допуски к разным отдельным эндпоинтам."""
        if self.action in ('me', 'subscriptions', 'subscribe', 'avatar'):
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    @action(detail=False, methods=['PUT', 'DELETE'], url_path='me/avatar')
    def avatar(self, request):
        """Добавляет или удаляет аватар пользователя."""
        user = request.user
        if request.method == 'DELETE':
            user.avatar.delete()
            user.avatar = None
            user.save()
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        serializer = AvatarSerializer(instance=user, data=request.data)
        serializer.is_valid(raise_exception=True)
        user.avatar.delete()
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, url_path='subscriptions')
    def subscriptions(self, request):
        """Возвращает список на кого подписан."""
        following = User.objects.filter(
            following__user=request.user).order_by('id')
        page = self.paginate_queryset(following)
        serializer = UserSubscriptionsSerializer(
            instance=page, many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)

    @action(detail=True, methods=['POST', 'DELETE'], url_path='subscribe')
    def subscribe(self, request, id=None):
        """Позволяет подписаться и отписаться на другого пользователя."""
        user = request.user
        following = get_object_or_404(User, id=id)
        follow = Follow.objects.filter(user=user, following=following)
        if request.method == 'DELETE':
            return delete_or_400(follow,
                                 'Вы не были подписаны на этого пользователя')
        if follow.exists():
            return exists_then_400('Вы уже подписаны на этого пользователя')
        if user == following:
            return Response(
                {'errors': 'Нельзя подписываться на самого себя'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        Follow.objects.create(user=user, following=following)
        serializer = UserSubscriptionsSerializer(
            instance=following, context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class IngredientViewSer(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    """Представление тэгов."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = (IngredientSearchFilter,)
    search_fields = ('^name',)


class TagViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    """Представление тэгов."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class RecipeViewSet(ModelViewSet):
    """Представление рецептов."""

    queryset = Recipe.objects.all()
    http_method_names = ('get', 'post', 'patch', 'delete')
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilterSet

    def get_permissions(self):
        """Переопределяет допуски к разным отдельным эндпоинтам."""
        if self.action in (
            'create', 'favorite', 'shopping_cart', 'download_shopping_cart',
        ):
            self.permission_classes = [IsAuthenticated]
        if self.action in ('partial_update', 'destroy'):
            self.permission_classes = [IsAuthenticated, IsAdminOrAuthor]
        return super().get_permissions()

    def get_serializer_class(self):
        """В зависимости от метода запроса."""
        if self.action in ('create', 'partial_update'):
            return RecipeWriteSerializer
        return RecipeReadSerializer

    def perform_create(self, serializer):
        """Автоматически сохраняет в пользователя в поле "автор"."""
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['POST', 'DELETE'], url_path='favorite')
    def favorite(self, request, pk=None):
        """Позволяет добавлять рецепты в избранные."""
        user = request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        favorite = Favoritism.objects.filter(user=user, recipe=recipe)
        if request.method == 'DELETE':
            return delete_or_400(favorite, 'Рецепт не был в избранном.')
        if favorite.exists():
            return exists_then_400('Вы уже добавили этот рецепт в избранное')
        Favoritism.objects.create(user=user, recipe=recipe)
        serializer = RecipeShortSerializer(
            instance=recipe, context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['POST', 'DELETE'], url_path='shopping_cart')
    def shopping_cart(self, request, pk=None):
        """Позволяет добавлять рецепты в избранные."""
        user = request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        shop = ShoppingCart.objects.filter(user=user, recipe=recipe)
        if request.method == 'DELETE':
            return delete_or_400(shop,
                                 'Этот рецепт не был в корзине')
        if shop.exists():
            return exists_then_400('Этот рецепт уже в корзине')
        ShoppingCart.objects.create(user=user, recipe=recipe)
        serializer = RecipeShortSerializer(
            instance=recipe, context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['Get'], url_path='download_shopping_cart')
    def download_shopping_cart(self, request):
        """Отдаст пользователю файл с его списком покупок."""
        ingredient_list_qs = RecipeIngredient.objects.filter(
            recipe__shop__user=request.user,
        )
        ingredient_list = [str(i).rsplit(' ', 1) for i in ingredient_list_qs]
        list_for_file = {}
        for element in ingredient_list:
            if element[0] in list_for_file:
                list_for_file[element[0]] += int(element[1])
            else:
                list_for_file[element[0]] = int(element[1])
        file_txt = [
            f'{ingredient.capitalize()} - {amount}\n'
            for ingredient, amount in list_for_file.items()
        ]
        return HttpResponse(file_txt, content_type='text/plain')

    @action(detail=True, url_path='get-link')
    def get_link(self, request, pk=None):
        """Возвращает короткую ссылку на рецепт."""
        short_link_recipe = ShortLink.objects.filter(recipe=pk)
        if not short_link_recipe.exists():
            recipe = get_object_or_404(Recipe, pk=pk)
            short_link_recipe = recipe.short_link()
        else:
            short_link_recipe = short_link_recipe.first()
        return Response(
            {'short-link': f'http{HTTPS}://{DOMAIN_NAME}'
                           f'/s/{short_link_recipe.short}/'},
            status=status.HTTP_200_OK
        )


@api_view(['GET'])
def redirect_short_link(request, short):
    """Обрабатывает короткие ссылки."""
    recipe_short_link = get_object_or_404(ShortLink, short=short)
    recipe_id = recipe_short_link.recipe.id
    substring = '/api' if LOCALLY else ''
    return redirect(
        f'http{HTTPS}://{DOMAIN_NAME}{substring}/recipes/{recipe_id}/'
    )
