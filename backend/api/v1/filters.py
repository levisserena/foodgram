import django_filters
from django_filters import FilterSet
from django_filters.filters import ModelMultipleChoiceFilter
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

    class Meta:
        """Метаданные."""

        model = Recipe
        fields = ('tags',)


# class RecipeForSubscriptionsFilterSet(FilterSet):
#     """Фильтр для отображения списка подписок."""

#     recipes = ModelMultipleChoiceFilter(
#         queryset=Tag.objects.all(),
#         field_name='tags__slug',
#         to_field_name='slug',
#     )

#     class Meta:
#         """Метаданные."""

#         model = User
#         fields = ('tags',)
