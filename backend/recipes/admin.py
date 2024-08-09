from django.contrib.admin import display, ModelAdmin, register, TabularInline
from django.utils.safestring import mark_safe

from backend.settings import EXTRA_TABULAR_INLINE
from users.models import User
from .models import Favoritism, Ingredient, Recipe, ShopingCart, ShortLink, Tag


class TagsInline(TabularInline):
    """Позволит в зоне администрирования в рецептах выбирать тэги."""

    model = Recipe.tags.through
    extra = EXTRA_TABULAR_INLINE
    verbose_name = 'Тэг к рецепту'
    verbose_name_plural = 'Тэги'


class IngredientsInline(TabularInline):
    """Позволит в зоне администрирования в рецептах выбирать ингридиенты."""

    model = Recipe.ingredients.through
    extra = EXTRA_TABULAR_INLINE
    verbose_name = 'Ингредиент к рецепту'
    verbose_name_plural = 'Ингредиенты'


@register(Recipe)
class RecipeAdmin(ModelAdmin):
    """Для управления рецептами в админ зоне."""

    fields = (
        'author',
        'name',
        'get_favorites_counter',
        'text',
        'cooking_time',
        ('image', 'get_html_image'),
    )
    list_display = ('id', 'name', 'author')
    list_display_links = ('id', 'name')
    list_filter = ('tags',)
    readonly_fields = (
        'get_html_image',
        'get_favorites_counter',  # убрать лишнее
    )
    inlines = (IngredientsInline, TagsInline)

    @display(description='Миниатюра')
    def get_html_image(self, object):
        """Возвращает миниатюру."""
        if object.image:
            return mark_safe(f'<img src="{object.image.url}" width=70>')
        return 'Нет аватара'

    @display(description='В избраном у ')
    def get_favorites_counter(self, object):
        """Возвращает счетчик добавлений этого рецепта в избранное."""
        count = '+100500'
        return f'{count} пользователей.'


@register(Tag)
class TagAdmin(ModelAdmin):
    """Для управления тэгами в админ зоне."""

    fields = ('name', 'slug')
    list_display = ('id', 'name', 'slug')
    list_display_links = ('id', 'name', 'slug')
    search_fields = ('name', 'slug')
    ordering = ('name',)


@register(Ingredient)
class IngredientAdmin(ModelAdmin):
    """Для управления ингредиентами в админ зоне."""

    fields = ('name', 'measurement_unit')
    list_display = ('id', 'name', 'measurement_unit')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    ordering = ('name',)


@register(Favoritism)
class FavoritismAdmin(ModelAdmin):
    """Для управления добавления рецептов в избранное в админ зоне."""

    pass


@register(ShopingCart)
class ShopingCartAdmin(ModelAdmin):
    """Для управления добавления рецептов в корзину в админ зоне."""

    pass



@register(ShortLink)
class ShortLinkAdmin(ModelAdmin):
    """Для управления добавления рецептов в корзину в админ зоне."""

    pass
