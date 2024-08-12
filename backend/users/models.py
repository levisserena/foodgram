from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db.models import (CASCADE, EmailField, ForeignKey,
                              ImageField, Model, UniqueConstraint)
from django.utils.safestring import mark_safe


class UserFoodgram(AbstractUser):
    """Модель пользователей, для проекта Footgram."""

    REQUIRED_FIELDS = ('first_name', 'last_name')

    email = EmailField(
        verbose_name='Электронная почта',
        unique=True,
        blank=False,
        null=True,
        help_text=('Поле обязательное для заполнения. '
                   'Для каждого пользователя уникально.')
    )
    avatar = ImageField(
        verbose_name='Аватар',
        upload_to='users/',
        null=True,
        blank=True,
        default=None,
    )

    def __str__(self):
        """Строковое представление модели."""
        return f'{self.last_name} {self.first_name} ({self.username})'

    @property
    def get_html_avatar(self):
        """Возвращает миниатюру."""
        if self.avatar:
            return mark_safe(f'<img src="{self.avatar.url}" width=70>')
        return 'Нет аватара'


User = get_user_model()


class Follow(Model):
    """Модель для подписки на других пользователей."""

    user = ForeignKey(
        User,
        on_delete=CASCADE,
        verbose_name='Кто подписывался',
    )
    following = ForeignKey(
        User,
        on_delete=CASCADE,
        related_name='following',
        verbose_name='На кого подписывался',
    )

    class Meta:
        """Метаданные."""

        verbose_name = 'Подписки'
        verbose_name_plural = 'Подписки'
        constraints = [
            UniqueConstraint(
                fields=['user', 'following'],
                name='unique_user_following'
            ),
        ]

    def __str__(self):
        """Метод отвечающий за строковое представление объекта."""
        return f'{self.user} подписан на {self.following}'

    def clean(self):
        """Метод не разрешает подписаться на самого себя."""
        if self.user == self.following:
            raise ValidationError(
                'Подписываться самому на себя нельзя!'
            )
