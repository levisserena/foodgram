import django_filters
from django_filters import FilterSet
from django_filters.filters import ModelMultipleChoiceFilter, NumberFilter
from rest_framework.filters import OrderingFilter, SearchFilter

from backend.settings import SEARCH_PARAM
from recipes.models import Recipe, Tag
from users.models import User


class IngredientSearchFilter(SearchFilter):
    """Фильтр поиска для ингредиентов. Ищет по полю name."""

    search_param = SEARCH_PARAM


class RecipeFilterSet(FilterSet):
    """Фильтр для отображения списка рецептов."""

    tags = ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        field_name='tags__slug',
        to_field_name='slug',
    )
    is_in_shopping_cart = NumberFilter(method='filter_selection')
    is_favorited = NumberFilter(method='filter_selection')
    author = NumberFilter(method='filter_selection')

    class Meta:
        """Метаданные."""

        model = Recipe
        fields = ('tags',)

    def filter_selection(self, queryset, name, value):
        """Фильтрует в зависимости от запроса."""
        if name == 'is_in_shopping_cart' and value:
            return queryset.filter(shop__user=self.request.user)
        elif name == 'is_favorited' and value:
            return queryset.filter(favorit__user=self.request.user)
        elif name == 'author' and value:
            return queryset.filter(author=self.request.user)
        return queryset
