from django.db.models import Case, IntegerField, Q, Value, When
from django_filters.rest_framework import (BooleanFilter, CharFilter,
                                           FilterSet,
                                           ModelMultipleChoiceFilter,
                                           NumberFilter)

from recipes.models import Ingredient, Recipe, Tag


class IngredientFilter(FilterSet):
    """Фильтр поиска для ингредиентов. Ищет по полю name."""

    name = CharFilter(method='filter_name')

    class Meta:
        """Метаданные."""

        model = Ingredient
        fields = ('name',)

    def filter_name(self, queryset, name, value):
        """Фильтр для ингредиентов. Сначала идут те, что начинаются с value,
        после - которые только содержат value."""
        return queryset.filter(
            Q(name__istartswith=value) | Q(name__icontains=value)
        ).annotate(
            priority=Case(
                When(name__istartswith=value, then=Value(1)),
                default=Value(2),
                output_field=IntegerField(),
            )
        ).order_by('priority', 'name')


class RecipeFilterSet(FilterSet):
    """Фильтр для отображения списка рецептов."""

    tags = ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        field_name='tags__slug',
        to_field_name='slug',
    )
    is_in_shopping_cart = BooleanFilter(method='filter_is_in_shopping_cart')
    is_favorited = BooleanFilter(method='filter_is_favorited')
    author = NumberFilter(method='filter_author')

    class Meta:
        """Метаданные."""

        model = Recipe
        fields = ('tags',)

    def filter_is_in_shopping_cart(self, queryset, name, value):
        """Фильтр для отсеивания рецептов в корзине."""
        if value and self.request.user.is_authenticated:
            return queryset.filter(shop__user=self.request.user)
        return queryset

    def filter_is_favorited(self, queryset, name, value):
        """Фильтр для отсеивания рецептов в избранном."""
        if value and self.request.user.is_authenticated:
            return queryset.filter(favorite__user=self.request.user)
        return queryset

    def filter_author(self, queryset, name, value):
        """Фильтр для отсеивания рецептов конкретного пользователя."""
        if value:
            return queryset.filter(author_id=value)
        return queryset
