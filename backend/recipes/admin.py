from django.contrib.admin import display, ModelAdmin, register, TabularInline

from backend.settings import EXTRA_TABULAR_INLINE
from .models import (Favoritism, Ingredient, Recipe,
                     ShoppingCart, ShortLink, Tag)


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


class ImageMixin:
    """Возвращает миниатюру аватара."""

    @display(description='')
    def get_html_image(self, object):
        """Возвращает миниатюру картинки."""
        return object.get_html_image


class AvatarMixin:
    """Возвращает миниатюру аватара."""

    @display(description='')
    def get_html_avatar_user(self, object):
        """Возвращает миниатюру аватара."""
        return object.user.get_html_avatar


@register(Recipe)
class RecipeAdmin(ImageMixin, AvatarMixin, ModelAdmin):
    """Для управления рецептами в админ зоне."""

    fields = (('author', 'get_html_avatar_user'), 'name',
              'get_favorites_counter', 'text', 'cooking_time',
              ('image', 'get_html_image'))
    list_display = ('id', 'name', 'author')
    list_display_links = ('id', 'name')
    list_filter = ('tags',)
    readonly_fields = ('get_html_avatar_user', 'get_favorites_counter',
                       'get_html_image')
    inlines = (IngredientsInline, TagsInline)
    search_fields = ('name', 'author__username', 'author__first_name',
                     'author__last_name',)

    @display(description='В избранном у ')
    def get_favorites_counter(self, object):
        """Возвращает счетчик добавлений этого рецепта в избранное."""
        count = Favoritism.objects.filter(recipe=object).count()
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
class FavoritismAdmin(ImageMixin, AvatarMixin, ModelAdmin):
    """Для управления добавления рецептов в избранное в админ зоне."""

    fields = (('user', 'get_html_avatar_user'), ('recipe', 'get_html_image'))
    readonly_fields = ('get_html_avatar_user', 'get_html_image')
    search_fields = ('user__username', 'user__first_name',
                     'user__last_name', 'recipe__name')


@register(ShoppingCart)
class ShoppingCartAdmin(FavoritismAdmin):
    """Для управления добавления рецептов в корзину в админ зоне."""

    pass


@register(ShortLink)
class ShortLinkAdmin(ModelAdmin):
    """Для управления добавления рецептов в корзину в админ зоне."""

    fields = ('recipe', 'short')
    search_fields = ('recipe', 'short')
