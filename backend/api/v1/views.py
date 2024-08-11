import os

from django.contrib.auth.tokens import default_token_generator
from django.db.models import Avg
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import RetrieveAPIView, UpdateAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework_simplejwt.tokens import AccessToken

from backend.settings import DOMAIN_NAME, HTTPS, LOCALLY  # SHOPPING_CART
from recipes.models import (Favoritism,
                            Ingredient,
                            Recipe,
                            RecipeIngredient,
                            ShopingCart,
                            ShortLink,
                            Tag)
from recipes.utilities import get_short_link
from users.models import Follow, User
from .filters import IngredientSearchFilter, RecipeFilterSet
from .paginations import FootgramPageNumberPagination
from .serializers import (AvatarSerializer,
                          IngredientSerializer,
                          RecipeReadSerializer,
                          RecipeShortSerializer,
                          RecipeWriteSerializer,
                          TagSerializer,
                          UserFoodgramSerializer,
                          UserSubscriptionsSerializer)
from .utilities import delete_image


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
            if not follow.exists():
                return Response(
                    {'errors': 'Вы не были подписаны на пользователя '
                               f'{following.last_name} '
                               f'{following.first_name}'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            follow.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        if follow.exists():
            return Response(
                    {'errors': 'Вы уже подписаны на пользователя '
                               f'{following.last_name} '
                               f'{following.first_name}'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
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
            'create', 'partial_update', 'destroy',
            'favorite', 'shopping_cart', 'download_shopping_cart',
        ):
            self.permission_classes = [IsAuthenticated]
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
            if not favorite.exists():
                return Response(
                    {'errors': f'Рецепт {recipe.name} не был в избранном.'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            favorite.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        if favorite.exists():
            return Response(
                    {'errors': f'Вы уже добавили рецепт {recipe.name} в '
                               'избранное.'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
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
        shop = ShopingCart.objects.filter(user=user, recipe=recipe)
        if request.method == 'DELETE':
            if not shop.exists():
                return Response(
                    {'errors': f'Рецепт {recipe.name} не был в корзине.'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            shop.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        if shop.exists():
            return Response(
                    {'errors': f'Вы уже добавили рецепт {recipe.name} в '
                               'корзину.'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        ShopingCart.objects.create(user=user, recipe=recipe)
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
        return HttpResponse(
            file_txt,
            content_type='text/plain'
        )

    @action(detail=True, url_path='get-link')
    def get_link(self, request, pk=None):
        """Позволяет подписаться и отписаться на другого пользователя."""
        short_link_recipe = ShortLink.objects.filter(recipe=pk)
        if not short_link_recipe.exists():
            while True:
                short_link = get_short_link()
                if not ShortLink.objects.filter(short=short_link).exists():
                    recipe = get_object_or_404(Recipe, pk=pk)
                    new_short_link = ShortLink.objects.create(recipe=recipe,
                                                              short=short_link)
                    short_link_recipe = new_short_link.short
                    break
        else:
            short_link_recipe = short_link_recipe.first().short
        return Response(
            {'short-link': f'http{HTTPS}://{DOMAIN_NAME}'
                           f'/s/{short_link_recipe}/'},
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
