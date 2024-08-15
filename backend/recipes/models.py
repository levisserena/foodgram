from django.core.validators import MinValueValidator
from django.db.models import (CASCADE, CharField, DateTimeField, ForeignKey,
                              ImageField, IntegerField, ManyToManyField, Model,
                              SlugField, TextField, UniqueConstraint)
from django.utils.safestring import mark_safe

from backend.settings import (LENGTH_SHORT_LINK, LENGTH_TEXT_LONG,
                              LENGTH_TEXT_MEDIUM, LENGTH_TEXT_SHORT,
                              LENGTH_TEXT_SMALL, MIN_AMOUNT, MIN_COOKING_TIME)
from users.models import User
from .utilities import get_short_link


class Tag(Model):
    """Метка-тэг."""

    name = CharField(
        verbose_name='Метка-тэг',
        max_length=LENGTH_TEXT_SMALL,
        blank=False,
    )
    slug = SlugField(
        verbose_name='Слаг',
        max_length=LENGTH_TEXT_SMALL,
        blank=False,
        unique=True,
        help_text='Уникальный идентификатор тэга, '
        'разрешены символы латиницы, цифры, дефис и подчёркивание.',
    )

    class Meta:
        """Метаданные."""

        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        """Строковое представление экземпляра класса."""
        return f'{self.name}'


class Ingredient(Model):
    """Ингредиент."""

    name = CharField(
        verbose_name='Название',
        max_length=LENGTH_TEXT_MEDIUM,
        unique=True,
        blank=False,
    )
    measurement_unit = CharField(
        verbose_name='Единица измерения',
        max_length=LENGTH_TEXT_SHORT,
        blank=False,
    )

    class Meta:
        """Метаданные."""

        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        """Строковое представление экземпляра класса."""
        return f'{self.name}, {self.measurement_unit}'


class Recipe(Model):
    """Рецепт."""

    name = CharField(
        verbose_name='Название',
        max_length=LENGTH_TEXT_LONG,
        blank=False,
    )
    text = TextField(
        verbose_name='Описание',
        blank=False
    )
    author = ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=CASCADE)
    ingredients = ManyToManyField(
        Ingredient,
        verbose_name='Ингредиенты',
        related_name='recipe',
        through='RecipeIngredient',
        blank=True,
    )
    tags = ManyToManyField(
        Tag,
        verbose_name='Тэги',
        related_name='recipe',
        through='RecipeTag',
        blank=False,
    )
    cooking_time = IntegerField(
        verbose_name='Время приготовления в минутах',
        validators=[MinValueValidator(
            MIN_COOKING_TIME,
            message=f'Значение не может быть меньше чем {MIN_COOKING_TIME}',
        )],
        blank=False,
    )
    image = ImageField(
        verbose_name='Картина',
        upload_to='recipes/images/',
        null=True,
        blank=False,
        default=None,
    )
    created = DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата создания',
    )

    class Meta:
        """Метаданные."""

        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-created',)

    def __str__(self):
        """Строковое представление экземпляра класса."""
        return f'{self.name} (id: {self.id})'

    @property
    def get_html_image(self):
        """Возвращает миниатюру."""
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" width=70>')
        return 'Нет картинки'

    def save(self, force_insert=False, force_update=False,
             using=None, update_fields=None):
        """При сохранение нового рецепта, создаёт короткую ссылку."""
        instance = super().save(
            force_insert, force_update, using, update_fields
        )
        self.create_short_link()
        return instance

    def create_short_link(self):
        """Создаст короткую ссылку на рецепт."""
        while True:
            short_link = get_short_link()
            if not ShortLink.objects.filter(short=short_link).exists():
                result = ShortLink.objects.create(recipe=self,
                                                  short=short_link)
                break
        return result

    @property
    def short_link(self):
        """Создаст короткую ссылку на рецепт."""
        return self.create_short_link()


class RecipeTag(Model):
    """Связная таблица Рецепт и Тэг."""

    recipe = ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=CASCADE,
    )
    tag = ForeignKey(
        Tag,
        verbose_name='Тэг',
        on_delete=CASCADE,
    )

    class Meta:
        """Метаданные."""

        constraints = [
            UniqueConstraint(
                fields=['recipe', 'tag'],
                name='unique_recipe_tag'
            ),
        ]

    def __str__(self):
        """Строковое представление экземпляра класса."""
        return f'{self.recipe} {self.tag}'


class RecipeIngredient(Model):
    """Связная таблица Рецепт и Ингредиент."""

    recipe = ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        related_name='ingredient_amount',
        on_delete=CASCADE
    )
    ingredient = ForeignKey(
        Ingredient,
        verbose_name='Ингредиент',
        on_delete=CASCADE,
    )
    amount = IntegerField(
        verbose_name='Количество ингредиента',
        validators=[MinValueValidator(
            MIN_AMOUNT,
            message=f'Значение не может быть меньше чем {MIN_AMOUNT}',
        )],
        blank=False,
    )

    class Meta:
        """Метаданные."""

        constraints = [
            UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_recipe_ingredient'
            ),
        ]

    def __str__(self):
        """Строковое представление экземпляра класса."""
        return f'{self.ingredient} {self.amount}'


class Favoritism(Model):
    """Модель для добавления рецепта в избранное."""

    user = ForeignKey(
        User,
        on_delete=CASCADE,
        verbose_name='Пользователь',
    )
    recipe = ForeignKey(
        Recipe,
        on_delete=CASCADE,
        verbose_name='Рецепт',
        related_name='favorite',
    )

    class Meta:
        """Метаданные."""

        verbose_name = 'Таблица избранных рецептов'
        verbose_name_plural = 'Таблица избранных рецептов'
        constraints = [
            UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_user_recipe_in_favorite'
            ),
        ]

    def __str__(self):
        """Строковое представление экземпляра класса."""
        return (f'{self.user.__str__()} добавил в избранное рецепт '
                f'{self.recipe.name}.')


class ShoppingCart(Model):
    """Модель для добавления рецепта корзину."""

    user = ForeignKey(
        User,
        on_delete=CASCADE,
        verbose_name='Пользователь',
    )
    recipe = ForeignKey(
        Recipe,
        on_delete=CASCADE,
        verbose_name='Рецепт',
        related_name='shop',
    )

    class Meta:
        """Метаданные."""

        verbose_name = 'Таблица рецептов, добавленных в корзину'
        verbose_name_plural = 'Таблица рецептов, добавленных в корзину'
        constraints = [
            UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_user_recipe_in_shopping'
            ),
        ]

    def __str__(self):
        """Строковое представление экземпляра класса."""
        return (f'{self.user.__str__()} добавил в корзину рецепт '
                f'{self.recipe.name}.')


class ShortLink(Model):
    """Модель для хранение коротких ссылок рецептов."""

    recipe = ForeignKey(
        Recipe,
        on_delete=CASCADE,
        verbose_name='Рецепт',
    )
    short = CharField(
        verbose_name='Короткая ссылка',
        max_length=LENGTH_SHORT_LINK,
        unique=True,
        blank=False,
    )

    class Meta:
        """Метаданные."""

        verbose_name = 'Короткая ссылка'
        verbose_name_plural = 'Короткие ссылки на рецепты'

    def __str__(self):
        """Строковое представление экземпляра класса."""
        return (f'Короткая ссылка рецепта {self.recipe.name}: {self.short}')
