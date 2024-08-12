from rest_framework.pagination import PageNumberPagination

from backend.settings import PAGE_SIZE, PAGE_SIZE_QUERY_PARAM


class FootgramPageNumberPagination(PageNumberPagination):
    """Пагинатор для Footgram. Используется в settings."""

    page_size = PAGE_SIZE
    page_size_query_param = PAGE_SIZE_QUERY_PARAM
