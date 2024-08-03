from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db.models import (CASCADE,
                              CharField,
                              EmailField,
                              ForeignKey,
                              ImageField,
                              IntegerField,
                              ManyToManyField,
                              Model,
                              TextField,
                              SET_NULL,
                              SlugField)

from backend.settings import (INVALID_ESER_NAMES,
                              MIN_AMOUNT,
                              LENGTH_USERNAME,
                              LENGTH_TEXT_SMALL,
                              LENGTH_TEXT_SHORT,
                              LENGTH_TEXT_MEDIUM,
                              LENGTH_TEXT_LONG)
from users.models import User


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
            MIN_AMOUNT,
            message=f'Значение не может быть меньше чем {MIN_AMOUNT}',
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

    class Meta:
        """Метаданные."""

        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        """Строковое представление экземпляра класса."""
        return f'{self.name}'


class RecipeTag(Model):
    """Связная таблица Рецепт и Тэг."""

    recipe = ForeignKey(
        Recipe,
        on_delete=CASCADE,
    )
    tag = ForeignKey(
        Tag,
        verbose_name='Тэг',
        on_delete=CASCADE,
    )

    def __str__(self):
        """Строковое представление экземпляра класса."""
        return f'{self.recipe} {self.tag}'


class RecipeIngredient(Model):
    """Связная таблица Рецепт и Ингредиент."""

    recipe = ForeignKey(
        Recipe,
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

    def __str__(self):
        """Строковое представление экземпляра класса."""
        return f'{self.ingredient} {self.amount}'
