from rest_framework.pagination import PageNumberPagination

from backend.settings import PAGE_SIZE, PAGE_SIZE_QUERY_PARAM


class FootgramPageNumberPagination(PageNumberPagination):
    """Пагинатор для Footgram."""

    page_size = PAGE_SIZE
    page_size_query_param = PAGE_SIZE_QUERY_PARAM


class RecipeForSubscriptionsPagination(PageNumberPagination):
    """Пагинатор для рецептов в подписках."""

    page_size = 3
    page_size_query_param = 'recipes_limit'
